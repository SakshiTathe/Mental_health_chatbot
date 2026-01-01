
let str='I am arjun'
let splits= str.split(' ').reverse();
console.log(splits)
splits.forEach((iteam)=>{
  iteam.split('').reverse().join('');
  console.log(iteam)
})