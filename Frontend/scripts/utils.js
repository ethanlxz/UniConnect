import axios from 'axios';

async function makeRequest(apiUrl, params = {}, payload = null, method = 'GET') {
	const config = {
		method: method.toLowerCase(),
		url: apiUrl,
		params: method.toUpperCase() === 'GET' ? params : {},
		data: method.toUpperCase() === 'POST' ? payload : null,
		headers: {
			'Content-Type': 'application/json'
		}
	};
	const response = await axios(config);
	return response.data;
}