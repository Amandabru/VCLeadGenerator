import AspectRatio from '@mui/joy/AspectRatio';
import Card from '@mui/joy/Card';
import CardContent from '@mui/joy/CardContent';
import CardOverflow from '@mui/joy/CardOverflow';
import Typography from '@mui/joy/Typography';
import './CardComponent.css';
import { CgProfile } from 'react-icons/cg';
import { MdOutlinePlace } from 'react-icons/md';
import { useState, useEffect} from 'react';
import { IoChevronBackOutline } from 'react-icons/io5';
import profile from '../assets/profile.png';
import {AiTwotoneHeart} from 'react-icons/ai';
import { useDispatch } from 'react-redux';
import { unsaveCompany } from '../redux/features/savedCompaniesSlice.js';
import { useNavigate } from 'react-router-dom';

function CardComponent({company, isLiked})  {

    const [isClicked, setIsClicked] = useState(false);
    const [selectedName, setSelectedName] = useState('');
    const dispatch = useDispatch();
    const navigateTo = useNavigate();

    useEffect(() => {
      setIsClicked(false);
    }, [company]);

    const handleNameClick = (name) => {
      setSelectedName(name);
      setIsClicked(true);
    };

    const handleBackClick = () => {
      setIsClicked(false);
    };

    const handleUnsaveClick = () => {
      dispatch(unsaveCompany(company));
      navigateTo('/saved');  
    };

    return (
      <div className='card'>
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
          className={`animation ${isClicked ? 'left-side-alt' : 'left-side'}`}
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
              <div style={{display: 'flex', flexDirection: 'row',  alignItems: 'baseline', justifyContent: 'space-between' }}>
                <Typography fontFamily="'Poppins', sans-serif" fontSize="xl4" fontWeight="xl" textColor="#fff">
                    {company.name}
                </Typography>
                {isLiked ? <AiTwotoneHeart className='heart' size={30} color="#58A894" onClick={handleUnsaveClick} /> : null}
              </div>
                <AspectRatio sx={{ mt: 1 }} ratio="19/8" objectFit="contain" variant="plain">
                    <img
                    alt=""
                    src={company.image}
                    />
                </AspectRatio>
                <div style={{display: 'flex', alignItems: 'center', }}>
                    <Typography className="tag" fontSize="0.8rem" fontFamily="'Poppins', sans-serif" textColor="#fff" sx={{ mt: 5 }}>
                        {company.industry}
                    </Typography>
                    <div style={{ display: 'flex', flexDirection:'row', marginLeft: 'auto', alignItems: 'center', marginRight: '1rem'}}>
                      <Typography fontSize="0.8rem" fontFamily="'Poppins', sans-serif" textColor="#fff" sx={{ mt: 5}}>
                          <MdOutlinePlace size={15}/> {company.location}
                      </Typography>
                      <Typography fontSize="0.8rem" fontFamily="'Poppins', sans-serif" textColor="#fff" sx={{ mt: 5, marginLeft: '1rem'}}>
                          Founded in {company.founded}
                      </Typography>
                    </div>
                </div>
                <Typography fontSize="0.77rem" fontFamily="'Poppins', sans-serif" textColor="#fff" sx={{ mt: 2}}>
                    {company.business}
                </Typography>
                <div style={{display: 'flex', flexDirection: 'row', gap: '2rem' }}>
                  <Typography fontFamily="'Poppins', sans-serif" fontSize="0.9rem" textColor="#fff" sx={{ mt: 2 }}>
                      <a className='website' href={company.website} rel="noreferrer" target='_blank' style={{ color: 'white', textDecoration: 'none', transition: 'color 0.2s'  }}>
                          Website
                      </a>
                  </Typography>
                  <Typography fontFamily="'Poppins', sans-serif" fontSize="0.9rem" textColor="#fff" sx={{ mt: 2 }}>
                      <a className='website' href={company.linkedIn} rel="noreferrer" target='_blank' style={{ color: 'white', textDecoration: 'none', transition: 'color 0.2s'  }}>
                          LinkedIn
                      </a>
                  </Typography>
                </div>
            </div>
            )}

          {isClicked && (
            <div style={{ zIndex: 999 }}>
              <IoChevronBackOutline color="#fff" onClick={handleBackClick} style={{cursor:'pointer'}}/>
              <AspectRatio  sx={{ mt: 4 }} ratio="19/8" objectFit="contain" variant="plain">
                  <img
                  alt=""
                  src={profile}
                  />
              </AspectRatio>
              <div className="divider" style={{ display: 'flex', marginTop: '2rem', marginLeft:'4rem', flexDirection: 'column'}}>
                <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'baseline', gap: '1rem'}}>
                  <Typography fontFamily="'Poppins', sans-serif" fontSize="xl2" textColor="#fff" >
                      {selectedName}
                  </Typography>
                  <Typography fontFamily="'Poppins', sans-serif" fontSize="0.9rem" textColor="#fff" >
                    <a href="" className='linkedIn' rel="noreferrer" target='_blank' style={{ color: 'white', textDecoration: 'none', transition: 'color 0.2s'  }}>LinkedIn</a>
                  </Typography>
                </div>
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
            <Typography textColor="#fff" sx={{ mt: 7 }} fontFamily="'Poppins', sans-serif" className="employees-title" level="title-lg">Founders</Typography>
            <Typography fontSize="sm" sx={{ mt: 0.5 }}>
            <ul className="custom-list">
                {company.employees.map((employee) => (
                    <li key={employee}><CgProfile/><a href="#1" onClick={() => {
                      handleNameClick(employee);
                    }}> {employee}</a></li>
                ))}
            </ul>
            </Typography>
            <Typography textColor="#fff" sx={{ mt: 0.5 }} fontFamily="'Poppins', sans-serif" fontSize="0.77rem">{company.founders}</Typography>
            <Typography textColor="#fff" sx={{ mt: 0.5 }} fontFamily="'Poppins', sans-serif" fontSize="0.77rem">Employees - {company.size}</Typography>
          </CardContent>

        </CardContent>
      </Card>
      </div>
    );
}

export default CardComponent;