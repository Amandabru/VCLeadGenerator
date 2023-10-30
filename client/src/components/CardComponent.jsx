import AspectRatio from '@mui/joy/AspectRatio';
import Card from '@mui/joy/Card';
import CardContent from '@mui/joy/CardContent';
import CardOverflow from '@mui/joy/CardOverflow';
import Typography from '@mui/joy/Typography';
import './CardComponent.css';
import { CgProfile } from 'react-icons/cg';
import { MdOutlinePlace } from 'react-icons/md';
import { useState } from 'react';

function CardComponent() {

    const [isClicked, setIsClicked] = useState(false);

    const handleNameClick = () => {
      setIsClicked(true);
    };

    return (
        <Card
        size="lg"
        orientation="horizontal"
        className="right-side"
        sx={{
          textAlign: 'left',
          maxWidth: '100%',
          width: 800,
          height: 500,
          overflow: 'auto',
          
        }}
      >
        <CardOverflow
          className={`animation ${isClicked ? 'left-side2' : 'left-side'}`}
          sx={{
            flex: '0 0 30rem',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-start',
            px: 'var(--Card-padding)',
          }}
        >
        {!isClicked && (
            <div>
                <Typography fontFamily="'Poppins', sans-serif" fontSize="xl4" fontWeight="xl" textColor="#fff">
                    QuantumFleet
                </Typography>
                <AspectRatio sx={{ mt: 1 }} ratio="19/8" objectFit="contain" variant="plain">
                    <img
                    alt=""
                    src="https://static.vecteezy.com/system/resources/previews/006/409/485/original/people-thinking-to-make-decision-problem-solving-and-find-creative-ideas-with-question-mark-in-flat-cartoon-background-for-poster-illustration-vector.jpg"
                    />
                </AspectRatio>
                <div style={{display: 'flex', alignItems: 'center', }}>
                    <Typography className="tag" fontSize="0.8rem" fontFamily="'Poppins', sans-serif" textColor="#fff" sx={{ mt: 5, marginRight: '1rem' }}>
                        TRANSPORTATION
                    </Typography>
                    <Typography fontSize="0.8rem" fontFamily="'Poppins', sans-serif" textColor="#fff" sx={{ mt: 5, marginLeft: '8rem', marginRight: '1rem' }}>
                        <MdOutlinePlace size={15}/> Stockholm
                    </Typography>
                    <Typography fontSize="0.8rem" fontFamily="'Poppins', sans-serif" textColor="#fff" sx={{ mt: 5}}>
                        Founded in 2022
                    </Typography>
                </div>
                <Typography fontSize="0.9rem" fontFamily="'Poppins', sans-serif" textColor="#fff" sx={{ mt: 2}}>
                    QuantumFleet is revolutionizing the transportation industry by developing a fleet of quantum-powered vehicles. 
                    Our cutting-edge quantum technology allows for near-instantaneous travel between locations, 
                    drastically reducing commute times and carbon emissions.
                </Typography>
                <Typography fontFamily="'Poppins', sans-serif" textColor="#fff" sx={{ mt: 4 }}>
                    <a href="">
                        Link to Website
                    </a>
                </Typography>
            </div>
            )}

          {isClicked && (
            <div style={{ zIndex: 999 }}>
              <AspectRatio sx={{ mt: 7 }} ratio="19/8" objectFit="contain" variant="plain">
                  <img
                  alt=""
                  src="https://static.vecteezy.com/system/resources/previews/006/409/485/original/people-thinking-to-make-decision-problem-solving-and-find-creative-ideas-with-question-mark-in-flat-cartoon-background-for-poster-illustration-vector.jpg"
                  />
              </AspectRatio>
              <div className="divider" style={{ display: 'flex', marginTop: '2rem', marginLeft:'4rem', flexDirection: 'column'}}>
                <Typography fontFamily="'Poppins', sans-serif" fontSize="xl2" textColor="#fff" >
                    Bo Tunnquist
                </Typography>
                <Typography sx={{ marginBottom:'1rem'}} fontSize="0.8rem" fontFamily="'Poppins', sans-serif" textColor="#fff">
                  50 years old
                </Typography>
              </div>
              <div className='divider' style={{ display: 'flex', flexDirection: 'column', marginLeft:'4rem'}}>
                <Typography fontSize="1rem" fontFamily="'Poppins', sans-serif" textColor="#fff">
                  Previous job roles
                </Typography>
                <Typography  fontSize="0.8rem" fontFamily="'Poppins', sans-serif" textColor="#fff">
                  VIP of commercial
                </Typography>
                <Typography sx={{ marginBottom:'1rem'}} fontSize="0.7rem" fontFamily="'Poppins', sans-serif" textColor="#fff">
                  Atlas Copco
                </Typography>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', marginLeft:'4rem'}}>
              <Typography fontSize="1rem" fontFamily="'Poppins', sans-serif" textColor="#fff">
                  Highest education
                </Typography>
                <Typography  fontSize="0.8rem" fontFamily="'Poppins', sans-serif" textColor="#fff">
                  Master of Science in Industrial Economy
                </Typography>
                <Typography sx={{ marginBottom:'1rem'}} fontSize="0.7rem" fontFamily="'Poppins', sans-serif" textColor="#fff">
                  Atlas Copco
                </Typography>
              </div>

            </div>
          )}
        </CardOverflow>
        <CardContent sx={{ gap: 1.5, minWidth: 200 }}>
          <CardContent>
            <Typography textColor="#fff" sx={{ mt: 7 }} fontFamily="'Poppins', sans-serif" className="employees-title" level="title-lg">Employees  -4</Typography>
            <Typography fontSize="sm" sx={{ mt: 0.5 }}>
            <ul className="custom-list">
                <li> <CgProfile/><a href="#1" onClick={handleNameClick}> Bo Tunnquist</a></li>
                <li><CgProfile/><a href="#1" onClick={handleNameClick}> Janne Jansson</a></li>
                <li><CgProfile/><a href="#1" onClick={handleNameClick}> Sofia Andersson</a></li>
                <li><CgProfile/><a href="#1" onClick={handleNameClick}> Kalle Karlsson</a></li>
            </ul>
            </Typography>
          </CardContent>

        </CardContent>
      </Card>
    );
}

export default CardComponent;