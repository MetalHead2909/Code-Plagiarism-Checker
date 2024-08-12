const express = require("express");
const bodyParser = require("body-parser");
const multer = require('multer');
const cors = require('cors');

const app = express();
app.use(cors());

app.set('view engine', 'ejs');

app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static(__dirname+"/public"));

const storage = multer.diskStorage({
    destination: function (req, file, callback) {
        callback(null, __dirname+"/uploads");
    },
    // Sets file(s) to be saved in folder in same directory
    filename: function (req, file, callback) {
        callback(null, file.originalname);
    }
    // Sets saved filename(s) to be original filename(s)
  })

// Set saved storage options:
const upload = multer({ storage: storage })


app.get("/", function(req, res){
    const lang = "Choose Language";
    res.render("homepage",{ languageChosen: lang});
});

app.get("/doccompare",function(req,res){
    res.render("doccompare",{})
})

app.post("/analysis",upload.array("pair"),function(req,res){
    console.log("app.js:",req.body.pair)
    var data={pair:req.body.pair};
    fetch('http://127.0.0.1:3000/doccompare',{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify(data),
        // checked:JSON.stringify(data),
    }).then(response => response.json())
    .then(result => {
        //console.log(result); 
        res.json(result);
    })
        .catch(error => console.log('Error Passing JSON: ',error));
    // res.json("Hello from app.js")
})

app.post("/api", upload.array("files"), (req, res) => {
    // Sets multer to intercept files named "files" on uploaded form data
    //console.log(req)
    console.log(req.body)
    console.log(req.body.files); // Logs form body values
    //console.log('check value:',req.checked);
    //console.log(req.files); // Logs any files
    var data={checked:req.body.files};
    fetch('http://127.0.0.1:3000/predict',{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify(data),
        // checked:JSON.stringify(data),
    }).then(response => response.json())
    .then(result => {
        console.log(result); 
        res.json(result);
    })
        .catch(error => console.log('Error Passing JSON: ',error));
});

app.post('/data',(req,res)=>{
    console.log(req.body);
    console.log(data);
    return 'Req from client rec'
})

app.listen(5000,function(){
    console.log("Server listening on port 5000");
})