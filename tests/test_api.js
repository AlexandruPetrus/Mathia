#!/usr/bin/env node

/**
 * Script de test des endpoints de l'API Mathia (version Node.js)
 * Usage: node tests/test_api.js
 */

const https = require('http');

const BASE_URL = 'http://localhost:3000/api';
const TEST_EMAIL = `test_${Date.now()}@example.com`;
const TEST_PASSWORD = 'test123456';
const TEST_NAME = 'Test User';

let TOKEN = '';
let USER_ID = '';
let FIRST_EXERCISE_ID = '';

// Couleurs pour le terminal
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

// Fonction pour faire des requêtes HTTP
function makeRequest(method, path, body = null, headers = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(BASE_URL + path);
    
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      }
    };

    const req = https.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          body: data ? JSON.parse(data) : null
        });
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    if (body) {
      req.write(JSON.stringify(body));
    }

    req.end();
  });
}

// Fonction pour afficher les résultats
function printTest(name, success) {
  const icon = success ? `${colors.green}✅` : `${colors.red}❌`;
  console.log(`${icon} ${name}${colors.reset}`);
}

function printInfo(text) {
  console.log(`${colors.blue}${text}${colors.reset}`);
}

function printWarning(text) {
  console.log(`${colors.yellow}${text}${colors.reset}`);
}

// Tests
async function runTests() {
  console.log('\n' + '='.repeat(70));
  console.log('🧪 TEST DE L\'API MATHIA (Node.js)');
  console.log('='.repeat(70) + '\n');
  console.log(`📍 URL de base: ${BASE_URL}`);
  console.log(`📧 Email de test: ${TEST_EMAIL}\n`);

  try {
    // TEST 1: Inscription
    console.log('='.repeat(70));
    console.log('TEST 1: POST /auth/signup - Créer un compte');
    console.log('='.repeat(70) + '\n');

    const signupData = {
      name: TEST_NAME,
      email: TEST_EMAIL,
      password: TEST_PASSWORD
    };

    console.log('📤 Requête:');
    console.log(`POST ${BASE_URL}/auth/signup`);
    console.log('Body:', { ...signupData, password: '***' });
    console.log('');

    const signupResponse = await makeRequest('POST', '/auth/signup', signupData);
    
    console.log(`📥 Réponse (HTTP ${signupResponse.statusCode}):`);
    console.log(JSON.stringify(signupResponse.body, null, 2));
    console.log('');

    if (signupResponse.statusCode === 201) {
      printTest('Inscription réussie', true);
      TOKEN = signupResponse.body.data.token;
      USER_ID = signupResponse.body.data.user.id;
      printInfo(`🔑 Token récupéré (${TOKEN.length} caractères)`);
      printInfo(`👤 User ID: ${USER_ID}`);
    } else {
      printTest('Inscription échouée', false);
      process.exit(1);
    }

    await sleep(1000);

    // TEST 2: Connexion
    console.log('\n' + '='.repeat(70));
    console.log('TEST 2: POST /auth/login - Obtenir un JWT');
    console.log('='.repeat(70) + '\n');

    const loginData = {
      email: TEST_EMAIL,
      password: TEST_PASSWORD
    };

    console.log('📤 Requête:');
    console.log(`POST ${BASE_URL}/auth/login`);
    console.log('Body:', { ...loginData, password: '***' });
    console.log('');

    const loginResponse = await makeRequest('POST', '/auth/login', loginData);
    
    console.log(`📥 Réponse (HTTP ${loginResponse.statusCode}):`);
    console.log(JSON.stringify(loginResponse.body, null, 2));
    console.log('');

    if (loginResponse.statusCode === 200) {
      printTest('Connexion réussie', true);
      TOKEN = loginResponse.body.data.token;
      printInfo('🔑 Nouveau token récupéré');
    } else {
      printTest('Connexion échouée', false);
    }

    await sleep(1000);

    // TEST 3: Récupérer les cours
    console.log('\n' + '='.repeat(70));
    console.log('TEST 3: GET /courses - Récupérer les cours');
    console.log('='.repeat(70) + '\n');

    console.log('📤 Requête:');
    console.log(`GET ${BASE_URL}/courses`);
    console.log(`Headers: Authorization: Bearer ${TOKEN.substring(0, 20)}...`);
    console.log('');

    const coursesResponse = await makeRequest('GET', '/courses', null, {
      'Authorization': `Bearer ${TOKEN}`
    });
    
    console.log(`📥 Réponse (HTTP ${coursesResponse.statusCode}):`);
    console.log(JSON.stringify(coursesResponse.body, null, 2));
    console.log('');

    if (coursesResponse.statusCode === 200) {
      printTest('Récupération des cours réussie', true);
      const coursesCount = coursesResponse.body.data.courses.length;
      printInfo(`📚 Nombre de cours: ${coursesCount}`);
    } else {
      printTest('Récupération des cours échouée', false);
    }

    await sleep(1000);

    // TEST 4: Lister tous les exercices
    console.log('\n' + '='.repeat(70));
    console.log('TEST 4: GET /exercises - Lister tous les exercices');
    console.log('='.repeat(70) + '\n');

    console.log('📤 Requête:');
    console.log(`GET ${BASE_URL}/exercises`);
    console.log(`Headers: Authorization: Bearer ${TOKEN.substring(0, 20)}...`);
    console.log('');

    const exercisesResponse = await makeRequest('GET', '/exercises', null, {
      'Authorization': `Bearer ${TOKEN}`
    });
    
    console.log(`📥 Réponse (HTTP ${exercisesResponse.statusCode}):`);
    console.log(JSON.stringify(exercisesResponse.body, null, 2));
    console.log('');

    if (exercisesResponse.statusCode === 200) {
      printTest('Récupération des exercices réussie', true);
      const exercisesCount = exercisesResponse.body.data.exercises.length;
      printInfo(`📝 Nombre d'exercices: ${exercisesCount}`);
      
      if (exercisesCount > 0) {
        FIRST_EXERCISE_ID = exercisesResponse.body.data.exercises[0].id;
        printInfo(`🎯 Premier exercice ID: ${FIRST_EXERCISE_ID}`);
      }
    } else {
      printTest('Récupération des exercices échouée', false);
    }

    await sleep(1000);

    // TEST 5: Filtrer les exercices
    console.log('\n' + '='.repeat(70));
    console.log('TEST 5: GET /exercises?courseId=1&difficulty=facile - Filtrer');
    console.log('='.repeat(70) + '\n');

    console.log('📤 Requête:');
    console.log(`GET ${BASE_URL}/exercises?courseId=1&difficulty=facile`);
    console.log(`Headers: Authorization: Bearer ${TOKEN.substring(0, 20)}...`);
    console.log('');

    const filteredResponse = await makeRequest('GET', '/exercises?courseId=1&difficulty=facile', null, {
      'Authorization': `Bearer ${TOKEN}`
    });
    
    console.log(`📥 Réponse (HTTP ${filteredResponse.statusCode}):`);
    console.log(JSON.stringify(filteredResponse.body, null, 2));
    console.log('');

    if (filteredResponse.statusCode === 200) {
      printTest('Filtrage des exercices réussi', true);
      const filteredCount = filteredResponse.body.data.exercises.length;
      printInfo(`📝 Exercices faciles du cours 1: ${filteredCount}`);
    } else {
      printTest('Filtrage des exercices échoué', false);
    }

    await sleep(1000);

    // TEST 6: Enregistrer une réponse
    console.log('\n' + '='.repeat(70));
    console.log('TEST 6: POST /attempts - Enregistrer une réponse');
    console.log('='.repeat(70) + '\n');

    const exerciseId = FIRST_EXERCISE_ID || 1;
    const attemptData = {
      exerciseId: exerciseId,
      userAnswer: 'Test answer'
    };

    console.log('📤 Requête:');
    console.log(`POST ${BASE_URL}/attempts`);
    console.log(`Headers: Authorization: Bearer ${TOKEN.substring(0, 20)}...`);
    console.log('Body:', attemptData);
    console.log('');

    const attemptResponse = await makeRequest('POST', '/attempts', attemptData, {
      'Authorization': `Bearer ${TOKEN}`
    });
    
    console.log(`📥 Réponse (HTTP ${attemptResponse.statusCode}):`);
    console.log(JSON.stringify(attemptResponse.body, null, 2));
    console.log('');

    if (attemptResponse.statusCode === 201) {
      printTest('Enregistrement de la réponse réussi', true);
      const isCorrect = attemptResponse.body.data.isCorrect;
      printInfo(`✓ Réponse enregistrée (Correcte: ${isCorrect})`);
    } else if (attemptResponse.statusCode === 404) {
      printWarning('⚠️  Exercice non trouvé (base de données vide?)');
      printTest('Test de tentative (exercice manquant)', true);
    } else {
      printTest('Enregistrement de la réponse échoué', false);
    }

    await sleep(1000);

    // TEST 7: Test sans authentification
    console.log('\n' + '='.repeat(70));
    console.log('TEST 7: Test sans authentification (doit échouer)');
    console.log('='.repeat(70) + '\n');

    console.log('📤 Requête:');
    console.log(`GET ${BASE_URL}/courses (sans token)`);
    console.log('');

    const unauthResponse = await makeRequest('GET', '/courses');
    
    console.log(`📥 Réponse (HTTP ${unauthResponse.statusCode}):`);
    console.log(JSON.stringify(unauthResponse.body, null, 2));
    console.log('');

    if (unauthResponse.statusCode === 401) {
      printTest('Protection JWT fonctionne correctement', true);
    } else {
      printTest('Protection JWT ne fonctionne pas!', false);
    }

    // Résumé
    console.log('\n' + '='.repeat(70));
    console.log('📊 RÉSUMÉ DES TESTS');
    console.log('='.repeat(70) + '\n');
    console.log(`${colors.green}✅ Tests terminés${colors.reset}\n`);
    console.log(`🔑 Token JWT généré: ${TOKEN.substring(0, 30)}...`);
    console.log(`👤 User ID: ${USER_ID}`);
    console.log(`📧 Email: ${TEST_EMAIL}\n`);
    console.log('💡 Vous pouvez exporter ce token:');
    console.log(`   export TOKEN="${TOKEN}"`);
    console.log(`   curl -H "Authorization: Bearer $TOKEN" ${BASE_URL}/courses\n`);
    console.log('='.repeat(70));

  } catch (error) {
    console.error(`${colors.red}❌ Erreur lors des tests:${colors.reset}`, error.message);
    process.exit(1);
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Lancer les tests
runTests();









