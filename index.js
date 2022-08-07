var express = require('express');
var cors = require('cors');
var app = express();

const corsOptions = {
  origin: [
    'http://localhost:3000',
  ],
};

app.use(cors(corsOptions));
app.use(express.static('public'));

function dataCut( data, page_id, step, length){
    var data = JSON.parse(data);
    //console.log(step + length)
    try{
        return data[page_id].slice(step,step+length)
    }catch{
        return data[page_id].slice(step,data[page_id].length)
    }
}

app.get('/car/:page_id', cors(corsOptions), function(req, res) {
  var page_id = req.params.page_id
  var rout = req.params.page_id.split('_')[0];
  var step = parseInt(req.query.step);
  var length = parseInt(req.query.length);
  const fs = require("fs");
  const content = fs.readFileSync(`./public/carDatas/${rout}/${page_id}.json`);
  if (step==length){
    console.log(JSON.parse(content.toString()))
    totalLength = JSON.parse(content.toString())[rout].length
    res.json({"length": totalLength})
  }else{
    var dataFrag = dataCut(content.toString(), rout, step, length)
    res.json(dataFrag)
  }
})

app.get('/carid/', cors(corsOptions), function(req, res) {
  var data
  var result = {}
  const fs = require('fs')
  const dir = './public/carDatas'
  const files = fs.readdirSync(dir)
  for (const file of files) {
    var datas = fs.readdirSync(dir+'/'+file)
    result[`${file}`] = []
    for (data of datas) {
      console.log(data)
      result[`${file}`].push(data)
    }
  }
  res.send(result)
}) 

app.listen(3001);