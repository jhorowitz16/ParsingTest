
echo "before"
echo $CLASSPATH
export CLASSPATH=.:/Downloads/json-simple-1.1.jar
source ~/.zshrc
echo "after"
echo $CLASSPATH
