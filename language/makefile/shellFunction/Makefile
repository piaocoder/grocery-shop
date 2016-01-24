DIR:=`pwd`
NEWDIR=$(shell pwd)
TEMP=
ADDDIR="xxx-$(NEWDIR)-bbbbbbbbbbb"
SRC="This is test string"

SRC0=
#SRC0+="+++++"
SRC0:=$(SRC0)"+++++"

SRC1=
SRC1+=/home/

install:
	@echo "========================测试反引号功能==================="
	echo $(DIR)
	@echo "\n========================测试shell功能==================="
	echo $(NEWDIR)
	@echo "\n========================测试变量赋值(echo是shell命令)==================="
	TEMP=$(SRC);echo $$TEMP
	@echo "\n========================测试特殊变量赋值(:=)==================="
	TEMP=$(SRC0);echo $$TEMP
	@echo "\n========================测试特殊变量赋值(+=)==================="
	TEMP=$(SRC1);echo $$TEMP
	@echo "\n========================测试特殊变量命令(:=或者+=)==================="
	#echo $$SRC1 有问题
	ls -l $(SRC1)
	@echo "\n========================测试反引号的变量赋值==================="
	TEMP=$(DIR)
	echo $(TEMP)  #相当于执行echo $($(DIR))
	@echo "\n========================测试shell函数的变量赋值==================="
	TEMP=$(NEWDIR)
	echo $(TEMP)  #相当于执行echo $($(DIR))，即echo $(XXXX)输出为空值
	@echo "\n========================测试shell函数的变量内嵌==================="
	echo $(ADDDIR)
