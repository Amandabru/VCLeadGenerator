import companyData from "../../data/companies.json";

async function getCompanies(amount) {
  // try {
  //   const response = await fetch(`http://localhost:8000/fetch/${amount}`);
  //   if (!response.ok) {
  //     throw new Error(`HTTP error! Status: ${response.status}`);
  //   }
  //   const data = await response.json();
  //   return data;
  // } catch (error) {
  //   console.error('Error:', error);
  //   return [];
  // }
  
  // mock data
  return companyData.slice(0, amount);;
}

export default getCompanies;