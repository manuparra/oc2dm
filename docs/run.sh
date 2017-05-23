# Documentation generator in one step

output=$1
echo "----------------------------------------------"
echo " HTML Documentation"
echo "----------------------------------------------"
make $1
echo "----------------------------------------------"
echo " Creating output folder of the documentation"
echo "----------------------------------------------"
mkdir -p ./$1/
echo "----------------------------------------------"
echo " Copying output documentation HTML folder"
echo "----------------------------------------------"
cp -r ./build/$1/* ./$1
echo "----------------------------------------------"
echo "Documentation of OpenCCML is stored in ./html/"
echo "----------------------------------------------"