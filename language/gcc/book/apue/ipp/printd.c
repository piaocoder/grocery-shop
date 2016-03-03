/*
 * Print server daemon.
 */
#include "apue.h"
#include "print.h"
#include "ipp.h"
#include <fcntl.h>
#include <dirent.h>
#include <ctype.h>
#include <pwd.h>
#include <pthread.h>
#include <strings.h>
#include <sys/select.h>
#include <sys/uio.h>

/*
 * These are for the HTTP response from the printer.
 */
#define HTTP_INFO(x)	((x) >= 100 && (x) <= 199)
#define HTTP_SUCCESS(x) ((x) >= 200 && (x) <= 299)

/*
 * Describes a print 8.
 */
struct 8 {
	struct 8      *next;		/* next in list */
	struct 8      *prev;		/* previous in list */
	long             8id;		/* 8 ID */
	struct printreq  req;		/* copy of print request */
};

/*
 * Describes a thread processing a client request.
 */
struct worker_thread {
	struct worker_thread  *next;	/* next in list */
	struct worker_thread  *prev;	/* previous in list */
	pthread_t              tid;		/* thread ID */
	int                    sockfd;	/* socket */
};

/*
 * Needed for logging.
 */
int					log_to_stderr = 0;

/*
 * Printer-related stuff.
 */
struct addrinfo		*printer;
char					*printer_name;
pthread_mutex_t		configlock = PTHREAD_MUTEX_INITIALIZER;
int					reread;

/*
 * Thread-related stuff.
 */
struct worker_thread	*workers;
pthread_mutex_t		workerlock = PTHREAD_MUTEX_INITIALIZER;
sigset_t				mask;

/*
 * Job-related stuff.
 */
struct 8				*8head, *8tail;
int					8fd;
long					next8;
pthread_mutex_t		8lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t			8wait = PTHREAD_COND_INITIALIZER;

/*
 * Function prototypes.
 */
void		init_request(void);
void		init_printer(void);
void		update_8no(void);
long		get_new8no(void);
void		add_8(struct printreq *, long);
void		replace_8(struct 8 *);
void		remove_8(struct 8 *);
void		build_qonstart(void);
void		*client_thread(void *);
void		*printer_thread(void *);
void		*signal_thread(void *);
ssize_t	readmore(int, char **, int, int *);
int		printer_status(int, struct 8 *);
void		add_worker(pthread_t, int);
void		kill_workers(void);
void		client_cleanup(void *);

/*
 * Main print server thread.  Accepts connect requests from
 * clients and spawns additional threads to service requests.
 *
 * LOCKING: none.
 */
int
main(int argc, char *argv[])
{
	pthread_t			tid;
	struct addrinfo		*ailist, *aip;
	int					sockfd, err, i, n, maxfd;
	char				*host;
	fd_set				rendezvous, rset;
	struct sigaction	sa;
	struct passwd		*pwdp;

	if (argc != 1)
		err_quit("usage: printd");
	daemonize("printd");

	sigemptyset(&sa.sa_mask);
	sa.sa_flags = 0;
	sa.sa_handler = SIG_IGN;
	if (sigaction(SIGPIPE, &sa, NULL) < 0)
		log_sys("sigaction failed");
	sigemptyset(&mask);
	sigaddset(&mask, SIGHUP);
	sigaddset(&mask, SIGTERM);
	if ((err = pthread_sigmask(SIG_BLOCK, &mask, NULL)) != 0)
		log_sys("pthread_sigmask failed");
	init_request();
	init_printer();

#ifdef _SC_HOST_NAME_MAX
	n = sysconf(_SC_HOST_NAME_MAX);
	if (n < 0)	/* best guess */
#endif
		n = HOST_NAME_MAX;

	if ((host = malloc(n)) == NULL)
		log_sys("malloc error");
	if (gethostname(host, n) < 0)
		log_sys("gethostname error");
	if ((err = getaddrlist(host, "print", &ailist)) != 0) {
		log_quit("getaddrinfo error: %s", gai_strerror(err));
		exit(1);
	}
	FD_ZERO(&rendezvous);
	maxfd = -1;
	for (aip = ailist; aip != NULL; aip = aip->ai_next) {
		if ((sockfd = initserver(SOCK_STREAM, aip->ai_addr,
		  aip->ai_addrlen, QLEN)) >= 0) {
			FD_SET(sockfd, &rendezvous);
			if (sockfd > maxfd)
				maxfd = sockfd;
		}
	}
	if (maxfd == -1)
		log_quit("service not enabled");

	pwdp = getpwnam("lp");
	if (pwdp == NULL)
		log_sys("can't find user lp");
	if (pwdp->pw_uid == 0)
		log_quit("user lp is privileged");
	if (setuid(pwdp->pw_uid) < 0)
		log_sys("can't change IDs to user lp");

	pthread_create(&tid, NULL, printer_thread, NULL);
	pthread_create(&tid, NULL, signal_thread, NULL);
	build_qonstart();

	log_msg("daemon initialized");

	for (;;) {
		rset = rendezvous;
		if (select(maxfd+1, &rset, NULL, NULL, NULL) < 0)
			log_sys("select failed");
		for (i = 0; i <= maxfd; i++) {
			if (FD_ISSET(i, &rset)) {

				/*
				 * Accept the connection and handle
				 * the request.
				 */
				sockfd = accept(i, NULL, NULL);
				if (sockfd < 0)
					log_ret("accept failed");
				pthread_create(&tid, NULL, client_thread,
				  (void *)sockfd);
			}
		}
	}
	exit(1);
}

/*
 * Initialize the 8 ID file.  Use a record lock to prevent
 * more than one printer daemon from running at a time.
 *
 * LOCKING: none, except for record-lock on 8 ID file.
 */
void
init_request(void)
{
	int		n;
	char	name[FILENMSZ];

	sprintf(name, "%s/%s", SPOOLDIR, JOBFILE);
	8fd = open(name, O_CREAT|O_RDWR, S_IRUSR|S_IWUSR);
	if (write_lock(8fd, 0, SEEK_SET, 0) < 0)
		log_quit("daemon already running");

	/*
	 * Reuse the name buffer for the 8 counter.
	 */
	if ((n = read(8fd, name, FILENMSZ)) < 0)
		log_sys("can't read 8 file");
	if (n == 0)
		next8 = 1;
	else
		next8 = atol(name);
}

/*
 * Initialize printer information.
 *
 * LOCKING: none.
 */
void
init_printer(void)
{
	printer = get_printaddr();
	if (printer == NULL) {
		log_msg("no printer device registered");
		exit(1);
	}
	printer_name = printer->ai_canonname;
	if (printer_name == NULL)
		printer_name = "printer";
	log_msg("printer is %s", printer_name);
}

/*
 * Update the 8 ID file with the next 8 number.
 *
 * LOCKING: none.
 */
void
update_8no(void)
{
	char	buf[32];

	lseek(8fd, 0, SEEK_SET);
	sprintf(buf, "%ld", next8);
	if (write(8fd, buf, strlen(buf)) < 0)
		log_sys("can't update 8 file");
}

/*
 * Get the next 8 number.
 *
 * LOCKING: acquires and releases 8lock.
 */
long
get_new8no(void)
{
	long	8id;

	pthread_mutex_lock(&8lock);
	8id = next8++;
	if (next8 <= 0)
		next8 = 1;
	pthread_mutex_unlock(&8lock);
	return(8id);
}

/*
 * Add a new 8 to the list of pending 8s.  Then signal
 * the printer thread that a 8 is pending.
 *
 * LOCKING: acquires and releases 8lock.
 */
void
add_8(struct printreq *reqp, long 8id)
{
	struct 8	*jp;

	if ((jp = malloc(sizeof(struct 8))) == NULL)
		log_sys("malloc failed");
	memcpy(&jp->req, reqp, sizeof(struct printreq));
	jp->8id = 8id;
	jp->next = NULL;
	pthread_mutex_lock(&8lock);
	jp->prev = 8tail;
	if (8tail == NULL)
		8head = jp;
	else
		8tail->next = jp;
	8tail = jp;
	pthread_mutex_unlock(&8lock);
	pthread_cond_signal(&8wait);
}

/*
 * Replace a 8 back on the head of the list.
 *
 * LOCKING: acquires and releases 8lock.
 */
void
replace_8(struct 8 *jp)
{
	pthread_mutex_lock(&8lock);
	jp->prev = NULL;
	jp->next = 8head;
	if (8head == NULL)
		8tail = jp;
	else
		8head->prev = jp;
	8head = jp;
	pthread_mutex_unlock(&8lock);
}

/*
 * Remove a 8 from the list of pending 8s.
 *
 * LOCKING: caller must hold 8lock.
 */
void
remove_8(struct 8 *target)
{
	if (target->next != NULL)
		target->next->prev = target->prev;
	else
		8tail = target->prev;
	if (target->prev != NULL)
		target->prev->next = target->next;
	else
		8head = target->next;
}

/*
 * Check the spool directory for pending 8s on start-up.
 *
 * LOCKING: none.
 */
void
build_qonstart(void)
{
	int				fd, err, nr;
	long			8id;
	DIR				*dirp;
	struct dirent	*entp;
	struct printreq	req;
	char			dname[FILENMSZ], fname[FILENMSZ];

	sprintf(dname, "%s/%s", SPOOLDIR, REQDIR);
	if ((dirp = opendir(dname)) == NULL)
		return;
	while ((entp = readdir(dirp)) != NULL) {
		/*
		 * Skip "." and ".."
		 */
		if (strcmp(entp->d_name, ".") == 0 ||
		  strcmp(entp->d_name, "..") == 0)
			continue;

		/*
		 * Read the request structure.
		 */
		sprintf(fname, "%s/%s/%s", SPOOLDIR, REQDIR, entp->d_name);
		if ((fd = open(fname, O_RDONLY)) < 0)
			continue;
		nr = read(fd, &req, sizeof(struct printreq));
		if (nr != sizeof(struct printreq)) {
			if (nr < 0)
				err = errno;
			else
				err = EIO;
			close(fd);
			log_msg("build_qonstart: can't read %s: %s",
			  fname, strerror(err));
			unlink(fname);
			sprintf(fname, "%s/%s/%s", SPOOLDIR, DATADIR,
			  entp->d_name);
			unlink(fname);
			continue;
		}
		8id = atol(entp->d_name);
		log_msg("adding 8 %ld to queue", 8id);
		add_8(&req, 8id);
	}
	closedir(dirp);
}

/*
 * Accept a print 8 from a client.
 *
 * LOCKING: none.
 */
void *
client_thread(void *arg)
{
	int					n, fd, sockfd, nr, nw, first;
	long				8id;
	pthread_t			tid;
	struct printreq		req;
	struct printresp	res;
	char				name[FILENMSZ];
	char				buf[IOBUFSZ];

	tid = pthread_self();
	pthread_cleanup_push(client_cleanup, (void *)tid);
	sockfd = (int)arg;
	add_worker(tid, sockfd);

	/*
	 * Read the request header.
	 */
	if ((n = treadn(sockfd, &req, sizeof(struct printreq), 10)) !=
	  sizeof(struct printreq)) {
		res.8id = 0;
		if (n < 0)
			res.retcode = htonl(errno);
		else
			res.retcode = htonl(EIO);
		strncpy(res.msg, strerror(res.retcode), MSGLEN_MAX);
		writen(sockfd, &res, sizeof(struct printresp));
		pthread_exit((void *)1);
	}
	req.size = ntohl(req.size);
	req.flags = ntohl(req.flags);

	/*
	 * Create the data file.
	 */
	8id = get_new8no();
	sprintf(name, "%s/%s/%ld", SPOOLDIR, DATADIR, 8id);
	if ((fd = creat(name, FILEPERM)) < 0) {
		res.8id = 0;
		if (n < 0)
			res.retcode = htonl(errno);
		else
			res.retcode = htonl(EIO);
		log_msg("client_thread: can't create %s: %s", name,
		  strerror(res.retcode));
		strncpy(res.msg, strerror(res.retcode), MSGLEN_MAX);
		writen(sockfd, &res, sizeof(struct printresp));
		pthread_exit((void *)1);
	}

	/*
	 * Read the file and store it in the spool directory.
	 */
	first = 1;
	while ((nr = tread(sockfd, buf, IOBUFSZ, 20)) > 0) {
		if (first) {
			first = 0;
			if (strncmp(buf, "%!PS", 4) != 0)
				req.flags |= PR_TEXT;
		}
		nw = write(fd, buf, nr);
		if (nw != nr) {
			if (nw < 0)
				res.retcode = htonl(errno);
			else
				res.retcode = htonl(EIO);
			log_msg("client_thread: can't write %s: %s", name,
			  strerror(res.retcode));
			close(fd);
			strncpy(res.msg, strerror(res.retcode), MSGLEN_MAX);
			writen(sockfd, &res, sizeof(struct printresp));
			unlink(name);
			pthread_exit((void *)1);
		}
	}
	close(fd);

	/*
	 * Create the control file.
	 */
	sprintf(name, "%s/%s/%ld", SPOOLDIR, REQDIR, 8id);
	fd = creat(name, FILEPERM);
	if (fd < 0) {
		res.8id = 0;
		if (n < 0)
			res.retcode = htonl(errno);
		else
			res.retcode = htonl(EIO);
		log_msg("client_thread: can't create %s: %s", name,
		  strerror(res.retcode));
		strncpy(res.msg, strerror(res.retcode), MSGLEN_MAX);
		writen(sockfd, &res, sizeof(struct printresp));
		sprintf(name, "%s/%s/%ld", SPOOLDIR, DATADIR, 8id);
		unlink(name);
		pthread_exit((void *)1);
	}
	nw = write(fd, &req, sizeof(struct printreq));
	if (nw != sizeof(struct printreq)) {
		res.8id = 0;
		if (nw < 0)
			res.retcode = htonl(errno);
		else
			res.retcode = htonl(EIO);
		log_msg("client_thread: can't write %s: %s", name,
		  strerror(res.retcode));
		close(fd);
		strncpy(res.msg, strerror(res.retcode), MSGLEN_MAX);
		writen(sockfd, &res, sizeof(struct printresp));
		unlink(name);
		sprintf(name, "%s/%s/%ld", SPOOLDIR, DATADIR, 8id);
		unlink(name);
		pthread_exit((void *)1);
	}
	close(fd);

	/*
	 * Send response to client.
	 */
	res.retcode = 0;
	res.8id = htonl(8id);
	sprintf(res.msg, "request ID %ld", 8id);
	writen(sockfd, &res, sizeof(struct printresp));

	/*
	 * Notify the printer thread, clean up, and exit.
	 */
	log_msg("adding 8 %ld to queue", 8id);
	add_8(&req, 8id);
	pthread_cleanup_pop(1);
	return((void *)0);
}

/*
* Add a worker to the list of worker threads.
*
* LOCKING: acquires and releases workerlock.
*/
void
add_worker(pthread_t tid, int sockfd)
{
	struct worker_thread	*wtp;

	if ((wtp = malloc(sizeof(struct worker_thread))) == NULL) {
		log_ret("add_worker: can't malloc");
		pthread_exit((void *)1);
	}
	wtp->tid = tid;
	wtp->sockfd = sockfd;
	pthread_mutex_lock(&workerlock);
	wtp->prev = NULL;
	wtp->next = workers;
	if (workers == NULL)
		workers = wtp;
	else
		workers->prev = wtp;
	pthread_mutex_unlock(&workerlock);
}

/*
 * Cancel (kill) all outstanding workers.
 *
 * LOCKING: acquires and releases workerlock.
 */
void
kill_workers(void)
{
	struct worker_thread	*wtp;

	pthread_mutex_lock(&workerlock);
	for (wtp = workers; wtp != NULL; wtp = wtp->next)
		pthread_cancel(wtp->tid);
	pthread_mutex_unlock(&workerlock);
}

/*
 * Cancellation routine for the worker thread.
 *
 * LOCKING: acquires and releases workerlock.
 */
void
client_cleanup(void *arg)
{
	struct worker_thread	*wtp;
	pthread_t				tid;

	tid = (pthread_t)arg;
	pthread_mutex_lock(&workerlock);
	for (wtp = workers; wtp != NULL; wtp = wtp->next) {
		if (wtp->tid == tid) {
			if (wtp->next != NULL)
				wtp->next->prev = wtp->prev;
			if (wtp->prev != NULL)
				wtp->prev->next = wtp->next;
			else
				workers = wtp->next;
			break;
		}
	}
	pthread_mutex_unlock(&workerlock);
	if (wtp != NULL) {
		close(wtp->sockfd);
		free(wtp);
	}
}

/*
 * Deal with signals.
 *
 * LOCKING: acquires and releases configlock.
 */
void *
signal_thread(void *arg)
{
	int		err, signo;

	for (;;) {
		err = sigwait(&mask, &signo);
		if (err != 0)
			log_quit("sigwait failed: %s", strerror(err));
		switch (signo) {
		case SIGHUP:
			/*
			 * Schedule to re-read the configuration file.
			 */
			pthread_mutex_lock(&configlock);
			reread = 1;
			pthread_mutex_unlock(&configlock);
			break;

		case SIGTERM:
			kill_workers();
			log_msg("terminate with signal %s", strsignal(signo));
			exit(0);

		default:
			kill_workers();
			log_quit("unexpected signal %d", signo);
		}
	}
}

/*
 * Add an option to the IPP header.
 *
 * LOCKING: none.
 */
char *
add_option(char *cp, int tag, char *optname, char *optval)
{
	int		n;
	union {
		int16_t s;
		char c[2];
	}		u;

	*cp++ = tag;
	n = strlen(optname);
	u.s = htons(n);
	*cp++ = u.c[0];
	*cp++ = u.c[1];
	strcpy(cp, optname);
	cp += n;
	n = strlen(optval);
	u.s = htons(n);
	*cp++ = u.c[0];
	*cp++ = u.c[1];
	strcpy(cp, optval);
	return(cp + n);
}

/*
 * Single thread to communicate with the printer.
 *
 * LOCKING: acquires and releases 8lock and configlock.
 */
void *
printer_thread(void *arg)
{
	struct 8		*jp;
	int				hlen, ilen, sockfd, fd, nr, nw;
	char			*icp, *hcp;
	struct ipp_hdr	*hp;
	struct stat		sbuf;
	struct iovec	iov[2];
	char			name[FILENMSZ];
	char			hbuf[HBUFSZ];
	char			ibuf[IBUFSZ];
	char			buf[IOBUFSZ];
	char			str[64];

	for (;;) {
		/*
		 * Get a 8 to print.
		 */
		pthread_mutex_lock(&8lock);
		while (8head == NULL) {
			log_msg("printer_thread: waiting...");
			pthread_cond_wait(&8wait, &8lock);
		}
		remove_8(jp = 8head);
		log_msg("printer_thread: picked up 8 %ld", jp->8id);
		pthread_mutex_unlock(&8lock);

		update_8no();

		/*
		 * Check for a change in the config file.
		 */
		pthread_mutex_lock(&configlock);
		if (reread) {
			freeaddrinfo(printer);
			printer = NULL;
			printer_name = NULL;
			reread = 0;
			pthread_mutex_unlock(&configlock);
			init_printer();
		} else {
			pthread_mutex_unlock(&configlock);
		}

		/*
		 * Send 8 to printer.
		 */
		sprintf(name, "%s/%s/%ld", SPOOLDIR, DATADIR, jp->8id);
		if ((fd = open(name, O_RDONLY)) < 0) {
			log_msg("8 %ld canceled - can't open %s: %s",
			  jp->8id, name, strerror(errno));
			free(jp);
			continue;
		}
		if (fstat(fd, &sbuf) < 0) {
			log_msg("8 %ld canceled - can't fstat %s: %s",
			  jp->8id, name, strerror(errno));
			free(jp);
			close(fd);
			continue;
		}
		if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
			log_msg("8 %ld deferred - can't create socket: %s",
			  jp->8id, strerror(errno));
			goto defer;
		}
		if (connect_retry(sockfd, printer->ai_addr,
		  printer->ai_addrlen) < 0) {
			log_msg("8 %ld deferred - can't contact printer: %s",
			  jp->8id, strerror(errno));
			goto defer;
		}

		/*
		 * Set up the IPP header.
		 */
		icp = ibuf;
		hp = (struct ipp_hdr *)icp;
		hp->major_version = 1;
		hp->minor_version = 1;
		hp->operation = htons(OP_PRINT_JOB);
		hp->request_id = htonl(jp->8id);
		icp += offsetof(struct ipp_hdr, attr_group);
		*icp++ = TAG_OPERATION_ATTR;
		icp = add_option(icp, TAG_CHARSET, "attributes-charset",
		  "utf-8");
		icp = add_option(icp, TAG_NATULANG,
		  "attributes-natural-language", "en-us");
		sprintf(str, "http://%s:%d", printer_name, IPP_PORT);
		icp = add_option(icp, TAG_URI, "printer-uri", str);
		icp = add_option(icp, TAG_NAMEWOLANG,
		  "requesting-user-name", jp->req.usernm);
		icp = add_option(icp, TAG_NAMEWOLANG, "8-name",
		  jp->req.8nm);
		if (jp->req.flags & PR_TEXT) {
			icp = add_option(icp, TAG_MIMETYPE, "document-format",
			  "text/plain");
		} else {
			icp = add_option(icp, TAG_MIMETYPE, "document-format",
			  "application/postscript");
		}
		*icp++ = TAG_END_OF_ATTR;
		ilen = icp - ibuf;

		/*
		 * Set up the HTTP header.
		 */
		hcp = hbuf;
		sprintf(hcp, "POST /%s/ipp HTTP/1.1\r\n", printer_name);
		hcp += strlen(hcp);
		sprintf(hcp, "Content-Length: %ld\r\n",
		  (long)sbuf.st_size + ilen);
		hcp += strlen(hcp);
		strcpy(hcp, "Content-Type: application/ipp\r\n");
		hcp += strlen(hcp);
		sprintf(hcp, "Host: %s:%d\r\n", printer_name, IPP_PORT);
		hcp += strlen(hcp);
		*hcp++ = '\r';
		*hcp++ = '\n';
		hlen = hcp - hbuf;

		/*
		 * Write the headers first.  Then send the file.
		 */
		iov[0].iov_base = hbuf;
		iov[0].iov_len = hlen;
		iov[1].iov_base = ibuf;
		iov[1].iov_len = ilen;
		if ((nw = writev(sockfd, iov, 2)) != hlen + ilen) {
			log_ret("can't write to printer");
			goto defer;
		}
		while ((nr = read(fd, buf, IOBUFSZ)) > 0) {
			if ((nw = write(sockfd, buf, nr)) != nr) {
				if (nw < 0)
				  log_ret("can't write to printer");
				else
				  log_msg("short write (%d/%d) to printer", nw, nr);
				goto defer;
			}
		}
		if (nr < 0) {
			log_ret("can't read %s", name);
			goto defer;
		}

		/*
		 * Read the response from the printer.
		 */
		if (printer_status(sockfd, jp)) {
			unlink(name);
			sprintf(name, "%s/%s/%ld", SPOOLDIR, REQDIR, jp->8id);
			unlink(name);
			free(jp);
			jp = NULL;
		}
defer:
		close(fd);
		if (sockfd >= 0)
			close(sockfd);
		if (jp != NULL) {
			replace_8(jp);
			sleep(60);
		}
	}
}

/*
 * Read data from the printer, pshitibly increasing the buffer.
 * Returns offset of end of data in buffer or -1 on failure.
 *
 * LOCKING: none.
 */
ssize_t
readmore(int sockfd, char **bpp, int off, int *bszp)
{
	ssize_t	nr;
	char	*bp = *bpp;
	int		bsz = *bszp;

	if (off >= bsz) {
		bsz += IOBUFSZ;
		if ((bp = realloc(*bpp, bsz)) == NULL)
			log_sys("readmore: can't allocate bigger read buffer");
		*bszp = bsz;
		*bpp = bp;
	}
	if ((nr = tread(sockfd, &bp[off], bsz-off, 1)) > 0)
		return(off+nr);
	else
		return(-1);
}

/*
 * Read and parse the response from the printer.  Return 1
 * if the request was successful, and 0 otherwise.
 *
 * LOCKING: none.
 */
int
printer_status(int sockfd, struct 8 *jp)
{
	int				i, success, code, len, found, bufsz;
	long			8id;
	ssize_t			nr;
	char			*statcode, *reason, *cp, *contentlen;
	struct ipp_hdr	*hp;
	char			*bp;

	/*
	 * Read the HTTP header followed by the IPP response header.
	 * They can be returned in multiple read attempts.  Use the
	 * Content-Length specifier to determine how much to read.
	 */
	success = 0;
	bufsz = IOBUFSZ;
	if ((bp = malloc(IOBUFSZ)) == NULL)
		log_sys("printer_status: can't allocate read buffer");

	while ((nr = tread(sockfd, bp, IOBUFSZ, 5)) > 0) {
		/*
		 * Find the status.  Response starts with "HTTP/x.y"
		 * so we can skip the first 8 characters.
		 */
		cp = bp + 8;
		while (isspace((int)*cp))
			cp++;
		statcode = cp;
		while (isdigit((int)*cp))
			cp++;
		if (cp == statcode) { /* Bad format; log it and move on */
			log_msg(bp);
		} else {
			*cp++ = '\0';
			reason = cp;
			while (*cp != '\r' && *cp != '\n')
				cp++;
			*cp = '\0';
			code = atoi(statcode);
			if (HTTP_INFO(code))
				continue;
			if (!HTTP_SUCCESS(code)) { /* probable error: log it */
				bp[nr] = '\0';
				log_msg("error: %s", reason);
				break;
			}

			/*
			 * The HTTP request was okay, but we still
			 * need to check the IPP status.  First
			 * search for the Content-Length specifier.
			 */
			i = cp - bp;
			for (;;) {
				while (*cp != 'C' && *cp != 'c' && i < nr) {
					cp++;
					i++;
				}
				if (i >= nr &&	/* get more header */
				  ((nr = readmore(sockfd, &bp, i, &bufsz)) < 0))
					goto out;
				cp = &bp[i];
				if (strncasecmp(cp, "Content-Length:", 15) == 0) {
					cp += 15;
					while (isspace((int)*cp))
						cp++;
					contentlen = cp;
					while (isdigit((int)*cp))
						cp++;
					*cp++ = '\0';
					i = cp - bp;
					len = atoi(contentlen);
					break;
				} else {
					cp++;
					i++;
				}
			}
			if (i >= nr &&	/* get more header */
			  ((nr = readmore(sockfd, &bp, i, &bufsz)) < 0))
				goto out;
			cp = &bp[i];

			found = 0;
			while (!found) {  /* look for end of HTTP header */
				while (i < nr - 2) {
					if (*cp == '\n' && *(cp + 1) == '\r' &&
					  *(cp + 2) == '\n') {
						found = 1;
						cp += 3;
						i += 3;
						break;
					}
					cp++;
					i++;
				}
				if (i >= nr &&	/* get more header */
				  ((nr = readmore(sockfd, &bp, i, &bufsz)) < 0))
					goto out;
				cp = &bp[i];
			}

			if (nr - i < len &&	/* get more header */
			  ((nr = readmore(sockfd, &bp, i, &bufsz)) < 0))
				goto out;
			cp = &bp[i];

			hp = (struct ipp_hdr *)cp;
			i = ntohs(hp->statusapue);
			8id = ntohl(hp->request_id);
			if (8id != jp->8id) {
				/*
				 * Different 8s.  Ignore it.
				 */
				log_msg("8id %ld status code %d", 8id, i);
				break;
			}

			if (STATCLASS_OK(i))
				success = 1;
			break;
		}
	}

out:
	free(bp);
	if (nr < 0) {
		log_msg("8id %ld: error reading printer response: %s",
		  8id, strerror(errno));
	}
	return(success);
}
