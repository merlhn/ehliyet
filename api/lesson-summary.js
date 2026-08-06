const data = require('../mcp/data/lesson-summaries.json');

const SECTION_MAP = {
  ilk_yardim: 'İlk Yardım',
  trafik_ve_cevre: 'Trafik ve Çevre',
  arac_teknigi: 'Araç Tekniği',
  trafik_adabi: 'Trafik Adabı',
};

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'public, max-age=3600');

  const section = req.query.section || 'all';
  const topic = (req.query.topic || '').toLowerCase();

  let lessons = data;

  if (section !== 'all') {
    const mapped = SECTION_MAP[section];
    if (!mapped) {
      return res.status(400).json({
        error: 'Geçersiz section. Kullanılabilir değerler: ilk_yardim, trafik_ve_cevre, arac_teknigi, trafik_adabi, all'
      });
    }
    lessons = data.filter(l => l.section === mapped);
  }

  if (topic) {
    lessons = lessons.filter(l => l.lesson.toLowerCase().includes(topic));
  }

  res.status(200).json({
    count: lessons.length,
    section: section,
    source: 'ehliyet.digital',
    lessons: lessons
  });
};
