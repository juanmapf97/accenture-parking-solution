import Link from 'next/link';

const cardStyle = {

};

const backgroundStyle = {

};

const Card = props => (
    <div className="main">
        <h3>{props.plate}<span className="date">{props.date}</span></h3>
        <div className="bkg-img"></div>
        <div className="inspect">Inspect visitor →</div>
        <style jsx>{`
            h3 {
                margin-left: 5%;
                font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Roboto","Oxygen","Ubuntu","Cantarell","Fira Sans","Droid Sans","Helvetica Neue",sans-serif;
            }
            .inspect {
                color: #0070f3;
                font-size: 14px;
                font-weight: 600;
                font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Roboto","Oxygen","Ubuntu","Cantarell","Fira Sans","Droid Sans","Helvetica Neue",sans-serif;
                margin-left: 5%;
                margin-top: 23px;
            }
            .date {
                color: #888;
                font-size: 18px;
                float: right;
                margin-right: 5%;
            }
            .main {
                height: 250px;
                width: 300px;
                border-radius: 8px;
                box-shadow: 0 5px 10px rgba(0,0,0,0.12);
                margin: 10px;
                position: relative;
            }
            .main:hover {
                cursor: pointer;
                box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            }
            .bkg-img {
                background: url(${props.image});
                background-position: center;
                background-repeat: no-repeat;
                height: 50%;
                width: 95%;
                margin: auto;
                background-size: cover;
                border-radius: 8px;
            }
            .bkg-img:hover {
                background: url(${props.closeup});
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
            }
            .info {
                border: 1px solid #cedcea;
                border-radius: 0px 0px 8px 8px;
                background-color: #efefef;
                height: 100px;
                padding-left: 100px;
                padding-top: 10px;
            }
            p {
                font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Roboto","Oxygen","Ubuntu","Cantarell","Fira Sans","Droid Sans","Helvetica Neue",sans-serif;;
            }
        `}</style>
    </div>
);

export default Card;