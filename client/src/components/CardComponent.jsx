import AspectRatio from '@mui/joy/AspectRatio';
import Card from '@mui/joy/Card';
import CardContent from '@mui/joy/CardContent';
import CardOverflow from '@mui/joy/CardOverflow';
import Typography from '@mui/joy/Typography';
import './CardComponent.css';
import { CgProfile } from 'react-icons/cg';
import { MdOutlinePlace } from 'react-icons/md';


function CardComponent() {
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
          className="left-side"
          sx={{
            flex: '0 0 30rem',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-start',
            px: 'var(--Card-padding)',
          }}
        >
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
        </CardOverflow>
        <CardContent sx={{ gap: 1.5, minWidth: 200 }}>
          <CardContent>
            <Typography textColor="#fff" sx={{ mt: 7 }} fontFamily="'Poppins', sans-serif" className="employees-title" level="title-lg">Employees  -4</Typography>
            <Typography fontSize="sm" sx={{ mt: 0.5 }}>
            <ul className="custom-list">
                <li> <CgProfile/><a href="#1"> Bo Tunnquist</a></li>
                <li><CgProfile/><a href="#1"> Janne Jansson</a></li>
                <li><CgProfile/><a href="#1"> Sofia Andersson</a></li>
                <li><CgProfile/><a href="#1"> Kalle Karlsson</a></li>
            </ul>
            </Typography>
          </CardContent>

        </CardContent>
      </Card>
    );
}

export default CardComponent;