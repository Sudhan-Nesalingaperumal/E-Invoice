addEventListener('fetch', (event) => {
    event.respondWith(handleRequest(event.request));
  });
  
  async function handleRequest(request) {
    try {
      const url = new URL(request.url);
      const paramName = url.searchParams.get('GST');
      
      const e_way_bill = [
        {
          'Gstin': '29AABCT1332L000',
          'email': 'saravanan@pganalytics.in',
          'username': 'mastergst',
          'password': 'Malli#123',
          'date': '01-12-2024',
        },
        {
          'Gstin': '33AQAPP7817N1ZG',
          'email': 'saravanan@pganalytics.in',
          'username': 'API_pga_pandiarajan',
          'password': 'PGA@tera2023',
          'date': '01-12-2024',
        },
        {
          'Gstin': '05AAACH6188F1ZM',
          'email': 'saravanan@pganalytics.in',
          'username': '05AAACH6188F1ZM',
          'password': 'abc123@@',
          'date': '01-12-2024',
        },
      ];
  
      let matchingItem = e_way_bill.find(item => item.Gstin === paramName);
      if (matchingItem) {
        const filteredData = [matchingItem]; 
        const jsonResponse = JSON.stringify(filteredData);
        return new Response(jsonResponse, {
          headers: { 'Content-Type': 'application/json' },
        });
      } else {
        const jsonData = JSON.stringify({
          result: 'No matching GST found',
        });
        return new Response(jsonData, {
          status: 300,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        });
      }
    } catch (error) {
      return new Response(error.message, { status: 500 });
    }
  }
  