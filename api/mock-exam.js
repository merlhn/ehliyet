const data = require('../mcp/data/questions.json');

// Gerçek MTSK sınav dağılımı: İY 12, TÇ 23, AT 9, TA 6 = 50
const DAGILIM = {
  'İlk Yardım': 12,
  'Trafik ve Çevre': 23,
  'Araç Tekniği': 9,
  'Trafik Adabı': 6,
};

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'no-cache');

  const textOnly = data.filter(q => !q.has_image);
  const exam = [];

  for (const [section, count] of Object.entries(DAGILIM)) {
    const pool = textOnly.filter(q => q.section === section);
    exam.push(...shuffle(pool).slice(0, count));
  }

  res.status(200).json({
    total: exam.length,
    duration_minutes: 45,
    pass_score: 70,
    pass_correct: 35,
    source: 'ehliyet.digital',
    distribution: DAGILIM,
    questions: exam
  });
};
