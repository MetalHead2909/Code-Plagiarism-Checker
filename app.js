const express = require("express");
const bodyParser = require("body-parser");
const multer = require('multer');
const cors = require('cors');

const app = express();
app.use(cors());

//const fs = require('fs');
//const AdminZip = require('adm-zip')

app.set('view engine', 'ejs');

app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static(__dirname+"/public"));

//const storage = multer.memoryStorage();
//const upload = multer({ storage });

const storage = multer.diskStorage({
    destination: function (req, file, callback) {
        callback(null, __dirname);
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
    res.render("homepage",{});
});

app.post("/api", upload.array("files"), (req, res) => {
    // Sets multer to intercept files named "files" on uploaded form data
    console.log(req.body); // Logs form body values
    console.log(req.files); // Logs any files
    //res.json({ message: "File(s) uploaded successfully" });
    var data={};
    //let finalresult = []
    fetch('http://127.0.0.1:3000/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(response => response.json())
    .then(result => {
        console.log(result); 
        res.json(result);
        //finalresult = result;
        //res.render("homepageedit",{groupingresults:result});
    })
        .catch(error => console.log('Error Passing JSON: ',error));
        //res.render("homepageedit",{groupingresults:finalresult});
});

// app.post("/upload",function(req,res){
//    console.log("app.js entered");
    //console.log(req)
    //console.log(req.file)
    //console.log(req.file['body'])
    //const zipFile = req.file;
    // console.log(req.body)
    // console.log(req.zipFile)
    // console.log(req.body.zipFile)
    // console.log(typeof(req.body))
    // const zip = new AdminZip(zipFile);
    // const zipEntries = zip.getEntries();

    // const txtFiles=[];
    // for(const zipEntry of zipEntries){
    //     if(zipEntry.entryName.endsWith('.txt')){
    //         const txtContent = zip.readAsText(zipEntry);

    //         txtFiles.push(txtContent);
    //     }
    // }
    // console.log(txtFiles);
// })

app.post('/data',(req,res)=>{
    console.log(req.body);
    console.log(data);
    return 'Req from client rec'
})

app.listen(5000,function(){
    console.log("Server listening on port 5000");
})