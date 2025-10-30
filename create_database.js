// Script pour créer la base de données mathia
require('dotenv').config();
const { Client } = require('pg');

async function createDatabase() {
  // Se connecter à la base postgres par défaut
  const client = new Client({
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'SSampeligreno_22',
    database: 'postgres' // Base par défaut
  });

  try {
    await client.connect();
    console.log('✅ Connecté à PostgreSQL');

    // Vérifier si la base existe déjà
    const result = await client.query(
      "SELECT 1 FROM pg_database WHERE datname = 'mathia'"
    );

    if (result.rows.length > 0) {
      console.log('✅ La base de données "mathia" existe déjà');
    } else {
      // Créer la base de données
      await client.query('CREATE DATABASE mathia');
      console.log('✅ Base de données "mathia" créée avec succès');
    }

    await client.end();
    console.log('\n🎉 Tout est prêt ! Vous pouvez maintenant lancer : npm run db:sync');
  } catch (error) {
    console.error('❌ Erreur:', error.message);
    
    if (error.code === 'ECONNREFUSED') {
      console.log('\n⚠️  PostgreSQL ne répond pas.');
      console.log('Vérifiez que le service "postgresql-x64-18" est démarré.');
    } else if (error.message.includes('password')) {
      console.log('\n⚠️  Mot de passe incorrect.');
      console.log('Éditez le fichier .env et mettez le bon mot de passe PostgreSQL.');
    }
    
    process.exit(1);
  }
}

createDatabase();




