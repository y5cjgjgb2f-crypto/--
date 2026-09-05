//alloc分配，Buffer内置的
let buf = Buffer.alloc(10);
//console.log(buf);
//allocUnsafe不安全速度快
let buf_2 = Buffer.allocUnsafe(10);
//console.log(buf_2);
//from
let buf_3 = Buffer.from('hello');
//let buf_4 = Buffer.from([1,216,152,33,55,4,5,0]);
console.log(buf_3);
//console.log(buf_4.toString());
console.log(buf_3[0]);
console.log(buf_3[0].toString(2));//进制转换
buf_3[1] = 55;//溢出361转成2进制会舍弃八位前面的位数，取后八位的数值
console.log(buf_3);
console.log(buf_3.toString());
