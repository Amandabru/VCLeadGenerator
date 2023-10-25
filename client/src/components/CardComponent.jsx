import AspectRatio from '@mui/joy/AspectRatio';
import Card from '@mui/joy/Card';
import CardContent from '@mui/joy/CardContent';
import CardOverflow from '@mui/joy/CardOverflow';
import Typography from '@mui/joy/Typography';
import './CardComponent.css';


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
            flex: '0 0 500px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-start',
            px: 'var(--Card-padding)',
          }}
        >
        <Typography fontFamily="'Poppins', sans-serif" fontSize="xl4" fontWeight="xl" textColor="#fff">
            Company Name
        </Typography>
        <AspectRatio sx={{ mt: 1 }} ratio="19/8" objectFit="contain" variant="plain">
            <img
              alt=""
              src="https://static.vecteezy.com/system/resources/previews/006/409/485/original/people-thinking-to-make-decision-problem-solving-and-find-creative-ideas-with-question-mark-in-flat-cartoon-background-for-poster-illustration-vector.jpg"
            />
        </AspectRatio>
        <div style={{display: 'flex', alignItems: 'center', }}>
            <Typography fontFamily="'Poppins', sans-serif" textColor="primary.200" sx={{ mt: 5, marginRight: '1rem' }}>
                Tag
            </Typography>
            <Typography fontFamily="'Poppins', sans-serif" textColor="primary.200" sx={{ mt: 5, marginLeft: '15rem', marginRight: '1rem' }}>
                Place
            </Typography>
            <Typography fontFamily="'Poppins', sans-serif" textColor="primary.200" sx={{ mt: 5}}>
                Founded in year
            </Typography>
        </div>
        <Typography fontFamily="'Poppins', sans-serif" textColor="primary.200" sx={{ mt: 4 }}>
            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the.
        </Typography>
        <Typography fontFamily="'Poppins', sans-serif" textColor="primary.200" sx={{ mt: 4 }}>
            <a href="">
                Link to Website
            </a>
        </Typography>
        </CardOverflow>
        <CardContent sx={{ gap: 1.5, minWidth: 200 }}>
          <CardContent>
            <Typography fontFamily="'Poppins', sans-serif" className="employees-title" level="title-lg">Employees  -4</Typography>
            <Typography fontSize="sm" sx={{ mt: 0.5 }}>
            <ul className="custom-list">
                <li>Jans Jansson</li>
                <li>Janne Janneson</li>
                <li>Johan Jonsson</li>
            </ul>
            </Typography>
          </CardContent>

        </CardContent>
      </Card>
    );
}

export default CardComponent;