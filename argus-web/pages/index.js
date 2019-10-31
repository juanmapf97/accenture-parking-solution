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
                    closeup={license.closeup}
                    date={license.date}/>
            ))}</div>
        <svg className="transparent" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#ff5500" fill-opacity="0.4" d="M0,128L30,122.7C60,117,120,107,180,112C240,117,300,139,360,133.3C420,128,480,96,540,74.7C600,53,660,43,720,80C780,117,840,203,900,240C960,277,1020,267,1080,250.7C1140,235,1200,213,1260,181.3C1320,149,1380,107,1410,85.3L1440,64L1440,320L1410,320C1380,320,1320,320,1260,320C1200,320,1140,320,1080,320C1020,320,960,320,900,320C840,320,780,320,720,320C660,320,600,320,540,320C480,320,420,320,360,320C300,320,240,320,180,320C120,320,60,320,30,320L0,320Z"></path></svg>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#ff5500" fill-opacity="0.2" d="M0,160L30,160C60,160,120,160,180,154.7C240,149,300,139,360,149.3C420,160,480,192,540,213.3C600,235,660,245,720,213.3C780,181,840,107,900,69.3C960,32,1020,32,1080,53.3C1140,75,1200,117,1260,149.3C1320,181,1380,203,1410,213.3L1440,224L1440,320L1410,320C1380,320,1320,320,1260,320C1200,320,1140,320,1080,320C1020,320,960,320,900,320C840,320,780,320,720,320C660,320,600,320,540,320C480,320,420,320,360,320C300,320,240,320,180,320C120,320,60,320,30,320L0,320Z"></path></svg>
        <svg className="normal" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#ff5500" fill-opacity="0.8" d="M0,128L30,133.3C60,139,120,149,180,128C240,107,300,53,360,69.3C420,85,480,171,540,176C600,181,660,107,720,80C780,53,840,75,900,101.3C960,128,1020,160,1080,170.7C1140,181,1200,171,1260,149.3C1320,128,1380,96,1410,80L1440,64L1440,320L1410,320C1380,320,1320,320,1260,320C1200,320,1140,320,1080,320C1020,320,960,320,900,320C840,320,780,320,720,320C660,320,600,320,540,320C480,320,420,320,360,320C300,320,240,320,180,320C120,320,60,320,30,320L0,320Z"></path></svg>
        <style jsx>{`
            div {
                padding: 25px;
                font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Roboto","Oxygen","Ubuntu","Cantarell","Fira Sans","Droid Sans","Helvetica Neue",sans-serif;
            }
            .transparent {
                position: absolute;
                width: 100%;
                bottom: 0;
                left: 0;
            }
            svg {
                position: absolute;
                width: 100%;
                bottom: 0;
                left: 0;
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
            objectDict[id]['date'] = jsonData.created_on;
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