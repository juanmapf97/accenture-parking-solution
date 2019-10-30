import Link from 'next/link'
import Card from '../components/Card';


export default function Blog() {
    return (
        <div className="main-container">
            <h1>Argus Parking Assistant</h1>
            <h2>Logged visitors</h2>
            <div className="card-container">
                <Card
                    plate="STH 18 - 65"
                    image="https://www.wsupercars.com/wallpapers/Audi/2014-Audi-RS7-Sportback-V8-1080.jpg"
                    closeup="https://www.oponeo.co.uk/gfx/Articles/license-plate.jpg"/>
                <Card
                    plate="STH 18 - 65"
                    image="https://www.wsupercars.com/wallpapers/Audi/2014-Audi-RS7-Sportback-V8-1080.jpg"
                    closeup="https://www.oponeo.co.uk/gfx/Articles/license-plate.jpg"/>
                <Card
                    plate="STH 18 - 65"
                    image="https://www.wsupercars.com/wallpapers/Audi/2014-Audi-RS7-Sportback-V8-1080.jpg"
                    closeup="https://www.oponeo.co.uk/gfx/Articles/license-plate.jpg"/>
                <Card
                    plate="STH 18 - 65"
                    image="https://www.wsupercars.com/wallpapers/Audi/2014-Audi-RS7-Sportback-V8-1080.jpg"
                    closeup="https://www.oponeo.co.uk/gfx/Articles/license-plate.jpg"/>
            </div>
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
}