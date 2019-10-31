import Link from 'next/link'
import Card from '../components/Card';
import fetch from 'isomorphic-unfetch';
var AWS = require('aws-sdk');

const Index = props => (
    <div className="main-container">
        <h1>Argus Parking Assistant</h1>
        <h2>Logged visitors</h2>
        <div className="card-container">{
            props.licenses.map(license => (
                <Card 
                    plate={license.plate}
                    image={license.image}
                    closeup={license.closeup}/>
            ))}</div>
        <style jsx>{`
            div {
                padding: 25px;
                font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Roboto","Oxygen","Ubuntu","Cantarell","Fira Sans","Droid Sans","Helvetica Neue",sans-serif;
            }
            .main-container {
                margin: auto;
                width: 65%;
                height: 100%;
            }
            .card-container {
                display: flex;
                flex-flow: row wrap;
                justify-contents: space-around;
                padding: 10px;
            }
            h1 {
                font-size: 32px;
            }
            h2 {
                color: #888;
                font-weight: 300;
            }
        `}</style>
    </div>
);

Index.getInitialProps = async function() {
    var s3 = new AWS.S3();
    var params = {
        Bucket: 'accenture-parking-solution',
        EncodingType: 'url'
    };
    var objectDict = {};
    var objectList = [];
    const baseAWSUrl = 'https://accenture-parking-solution.s3.us-east-2.amazonaws.com/';
    var res = s3.listObjects(params, async (err, data) => {
        if (err) console.log(err);
        else     console.log(data);
    });
    var data = await res.promise();
    for (var index = 0; index < data.Contents.length; index++) {
        var key = data.Contents[index].Key;
        var id = key.split('-')[0];
        var name = key.split('-')[1];
        if (objectDict[id] == undefined) {
            objectDict[id] = {}
        }
        if (name.includes('cropped')) {
            objectDict[id]['closeup'] = `${baseAWSUrl}${key}`;
        }
        else if (name.includes('full')) {
            objectDict[id]['image'] = `${baseAWSUrl}${key}`;
        }
        else {
            var res = await fetch(`${baseAWSUrl}${key}`);
            var jsonData = await res.json();
            objectDict[id]['plate'] = jsonData.plate;
        }
    }
    for (const id in objectDict) {
        if (objectDict.hasOwnProperty(id)) {
            const data = objectDict[id];
            objectList.push(data);
        }
    }
    return {
        licenses: objectList
    };
};

export default Index;