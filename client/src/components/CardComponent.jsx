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
        <Typography fontSize="xl4" fontWeight="xl" textColor="#fff">
            Company Name
        </Typography>
        <AspectRatio sx={{ mt: 1 }} ratio="19/8" objectFit="contain" variant="plain">
            <img
              alt=""
              src="https://static.vecteezy.com/system/resources/previews/006/409/485/original/people-thinking-to-make-decision-problem-solving-and-find-creative-ideas-with-question-mark-in-flat-cartoon-background-for-poster-illustration-vector.jpg"
            />
        </AspectRatio>
        <div style={{display: 'flex', alignItems: 'center' }}>
            <Typography textColor="primary.200" sx={{ mt: 4, marginRight: '1rem' }}>
                Tag
            </Typography>
            <Typography textColor="primary.200" sx={{ mt: 4, marginLeft: '15rem', marginRight: '1rem' }}>
                Place
            </Typography>
            <Typography textColor="primary.200" sx={{ mt: 4 }}>
                Founded in year
            </Typography>
        </div>
        <Typography textColor="primary.200" sx={{ mt: 4 }}>
            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the.
        </Typography>
        <Typography textColor="primary.200" sx={{ mt: 4 }}>
            <a href="">
                Link to Website
            </a>
        </Typography>
        </CardOverflow>
        <CardContent sx={{ gap: 1.5, minWidth: 200 }}>
          <CardContent>
            <Typography level="title-lg">Employees</Typography>
            <Typography fontSize="sm" sx={{ mt: 0.5 }}>
              <ul>
                <li>
                    Jans
                </li>
                <li>
                    Janne
                </li>
                <li>
                    Johan
                </li>
              </ul>
            </Typography>
          </CardContent>

        </CardContent>
      </Card>
    );
}

export default CardComponent;