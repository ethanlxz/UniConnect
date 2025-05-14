
async function makeRequest(apiUrl, params = {}, payload = null, method = 'GET') {
	const config = {
		method: method.toLowerCase(),
		url: "http://127.0.0.1:8000/" + apiUrl,
		params: method.toUpperCase() === 'GET' ? params : {},
		data: method.toUpperCase() === 'POST' ? payload : null,
		headers: {
			'Content-Type': 'application/json'
		}
	};
	const response = await axios(config);
	return response.data;
}