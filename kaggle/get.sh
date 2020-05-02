rm *.json

array=(
7w1bhaz6
bmsmegbs
7w1bhaz6
xsqgrd5l
56zhxd6e
atnz63pk
ofoqk100
k3f7ohzg
)

for i in "${array[@]}";do
    echo running ${i}
    curl http://tuna.cs.uwaterloo.ca:1234/gen/${i}?pageNumber=5 > ${i}.json
    # curl http://tuna.cs.uwaterloo.ca:1234/genDiff/${i} > ${i}.json
done;
