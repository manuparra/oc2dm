# Documentation generator in one step

echo "--> HTML Documentation"
make html
echo "--> Creating output folder of the documentation"
mkdir -p ./html/
echo "--> Copying output documentation HTML folder"
cp -r ./build/html/* ./html
echo "----------------------------------------------"
echo "Documentation of OpenCCML is stored in ./html/"
echo "----------------------------------------------"