#! /bin/sh

# :åå½å ä½ç¬¦
: ${username=`ls`}
echo $username

while test $# -gt 0; do
	echo 'what is wrong?'
	case $1 in
	--version | --vers)
		echo $1
		break
		;;
	--? | --wa)
		echo "??"
		break
		;;
	*)
		break
		;;
	esac
done

pwd
