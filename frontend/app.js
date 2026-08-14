const express = require('express');
const path = require('path');
const axios = require('axios');

// Frontend server for the EJS interface that talks to the Flask API.
const app = express();
const port = process.env.PORT || 3000;
const API_BASE_URL = process.env.API_BASE_URL || 'http://127.0.0.1:5000';

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Route: landing page for the login screen.
app.get('/', (req, res) => res.render('login'));

// Authenticate the user against the Flask backend before allowing access.
app.post('/login', async (req, res) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/login`, {
      username: req.body.username,
      password: req.body.password,
    });
    if (response.data.success) {
      res.redirect('/floors');
    } else {
      res.render('login', { error: 'Invalid login' });
    }
  } catch (error) {
    res.render('login', { error: 'Unable to reach backend' });
  }
});

app.get('/floors', async (req, res) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/floors`);
    res.render('floors', { items: response.data, title: 'Floors' });
  } catch (error) {
    res.render('floors', { items: [], title: 'Floors', error: 'Could not load floors' });
  }
});

app.post('/floors', async (req, res) => {
  await axios.post(`${API_BASE_URL}/floors`, req.body);
  res.redirect('/floors');
});

app.post('/floors/:id/delete', async (req, res) => {
  await axios.delete(`${API_BASE_URL}/floors/${req.params.id}`);
  res.redirect('/floors');
});

app.get('/rooms', async (req, res) => {
  try {
    const [roomsResponse, floorsResponse] = await Promise.all([
      axios.get(`${API_BASE_URL}/rooms`),
      axios.get(`${API_BASE_URL}/floors`),
    ]);
    res.render('rooms', { items: roomsResponse.data, floors: floorsResponse.data, title: 'Rooms' });
  } catch (error) {
    res.render('rooms', { items: [], floors: [], title: 'Rooms', error: 'Could not load rooms' });
  }
});

app.post('/rooms', async (req, res) => {
  await axios.post(`${API_BASE_URL}/rooms`, req.body);
  res.redirect('/rooms');
});

app.post('/rooms/:id/delete', async (req, res) => {
  await axios.delete(`${API_BASE_URL}/rooms/${req.params.id}`);
  res.redirect('/rooms');
});

app.get('/residents', async (req, res) => {
  try {
    const [residentsResponse, roomsResponse] = await Promise.all([
      axios.get(`${API_BASE_URL}/residents`),
      axios.get(`${API_BASE_URL}/rooms`),
    ]);
    const hasRooms = Array.isArray(roomsResponse.data) && roomsResponse.data.length > 0;
    res.render('residents', {
      items: residentsResponse.data,
      rooms: roomsResponse.data,
      title: 'Residents',
      error: hasRooms ? undefined : 'Create a room before adding a resident.'
    });
  } catch (error) {
    res.render('residents', { items: [], rooms: [], title: 'Residents', error: 'Could not load residents' });
  }
});

app.post('/residents', async (req, res) => {
  await axios.post(`${API_BASE_URL}/residents`, req.body);
  res.redirect('/residents');
});

app.post('/residents/:id/delete', async (req, res) => {
  await axios.delete(`${API_BASE_URL}/residents/${req.params.id}`);
  res.redirect('/residents');
});

app.listen(port, () => {
  console.log(`Frontend running on http://127.0.0.1:${port}`);
});
