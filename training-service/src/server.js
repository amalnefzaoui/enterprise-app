const express = require('express');
const cors = require('cors');
require('dotenv').config();

const { sequelize } = require('./models');
const coursesRouter = require('./routes/courses');
const enrollmentsRouter = require('./routes/enrollments');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

app.use('/api/courses', coursesRouter);
app.use('/api/enrollments', enrollmentsRouter);

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Training Service opérationnel' });
});

app.use((req, res) => {
  res.status(404).json({ error: 'Route non trouvée' });
});

async function start() {
  try {
    await sequelize.authenticate();
    console.log('✅ Connexion à la base de données réussie');

    await sequelize.sync({ alter: true });
    console.log('✅ Modèles synchronisés avec la base de données');

    app.listen(PORT, () => {
      console.log(`🚀 Training Service démarré sur le port ${PORT}`);
    });
  } catch (err) {
    console.error('❌ Erreur de démarrage:', err);
    process.exit(1);
  }
}

start();
