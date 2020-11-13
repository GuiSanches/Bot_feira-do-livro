const axios = require('axios');
const FileDownload = require('js-file-download');
const fs = require('fs');

const url = 'https://drive.google.com/uc?export=download&id=1DS7Vj5a4vUPD2T-Qi34OaCnpEr2EKsOr'

axios({
  url: url, //your url
  method: 'GET',
  responseType: 'blob', // important
}).then((response) => {
  // console.log(response)
  fs.writeFile("file.pdf", response.data, (err) => {
    if (err) console.log(err);
    console.log("Successfully Written to File.");
  });
  FileSaver.saveAs(response.data, 'file.pdf');
});