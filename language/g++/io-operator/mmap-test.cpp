#include <iostream>
#include <string.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <assert.h>

using namespace std;

inline size_t getFilesize(const char* filename) 
{
    struct stat st;

    stat(filename, &st);
    return st.st_size;
}

int main(int argc, char** argv) 
{
    size_t          filesize = 0;
    int             fd = 0, rc = -1;
    void           *mmappedData = NULL;
    char            buf[200];

    if (argc != 2) {
        cout << "Please input a filename!" << endl;
        return -1;
    }

    filesize = getFilesize(argv[1]);
    cout << "Input filename:" << argv[1] 
        << " File size is " << filesize << endl;

    fd = open(argv[1], O_RDONLY, 0);
    if (fd == -1) {
        cout << "Open file failed!" << endl;
        return -1;
    }

    //Execute mmap
    mmappedData = mmap(NULL, filesize, PROT_READ, 
            MAP_PRIVATE | MAP_POPULATE, fd, 0);
    if (mmappedData == MAP_FAILED) {
        cout << "Mmap failed!" << endl;
        return -1;
    }

    //Write the mmapped data to stdout (= FD #1)
    //write(1, mmappedData, filesize);
    memcpy(buf, mmappedData, 100);
    buf[100] = '\0';
    cout << "This first 100 bytes:" << buf << endl;

    //Cleanup
    rc = munmap(mmappedData, filesize);
    if (rc != 0) {
        cout << "Clean mmap failed!" << endl;
    }

    close(fd);
    return 0;
}
