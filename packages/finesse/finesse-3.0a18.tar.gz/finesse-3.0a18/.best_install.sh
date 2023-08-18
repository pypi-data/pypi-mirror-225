#!/bin/bash

# get working directory
CWD=`pwd`

# Install numpy (required for tests)
conda install pip numpy requests -y

# update finessetest repo
cd $FINESSE_TEST_DIR
git pull
cd $CWD
ln -s $FINESSE_TEST_DIR legacy_test

# Make mytest program
PYTEST="${CWD}/legacy_test/test3.py"
MYTEST="${CWD}/mytest"

# Build BESTDATASERVER URL
COMMIT=`git rev-parse HEAD`
HOST=$BESTDATASERVER
PRE="/filestorage/"
URI="/commit/${COMMIT}"

echo "#!/bin/bash" > $MYTEST
echo python $PYTEST '$1' "${HOST}${PRE}upload/test/"'$BEST_TEST_NUMBER'>> $MYTEST
chmod +x $MYTEST

# Make .best_env_var.sh on the fly as well
BESTENV=".best_env_var.sh"
echo "export MYTEST_DIR=${CWD}"/ >> $BESTENV
echo export PATH='${MYTEST_DIR}:$PATH' >> $BESTENV 

echo "Current Directory Structure"
ls -la
