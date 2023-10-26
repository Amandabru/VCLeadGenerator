
async function getCompanies(amount) {
  try {
    const response = await fetch(`/fetch/${amount}`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    return [];
  }
}

export default getCompanies;