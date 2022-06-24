

arr = [1,1,1,0,1,1,1,1,1,1,1,1,1,1]

count = 0
resultArr = []
for(let i = 0; i < arr.length; i ++){

    if(arr[i] == 0){
        count += 1
        
        if(i == arr.length -1){
            resultArr.push(count)
        }
        continue
    }
    else{
        if(count != 0){
            resultArr.push(count)
        }
        count = 0
    }
}

console.log(resultArr)