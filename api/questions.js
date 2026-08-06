const data = require('../mcp/data/questions.json');

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
  const count = Math.min(parseInt(req.query.count) || 10, 50);

  let questions = data.filter(q => !q.has_image);

  if (section !== 'all') {
    const mapped = SECTION_MAP[section];
    if (!mapped) {
      return res.status(400).json({
        error: 'Geçersiz section. Kullanılabilir değerler: ilk_yardim, trafik_ve_cevre, arac_teknigi, trafik_adabi, all'
      });
    }
    questions = questions.filter(q => q.section === mapped);
  }

  // Rastgele seç
  const shuffled = questions.sort(() => Math.random() - 0.5).slice(0, count);

  res.status(200).json({
    count: shuffled.length,
    section: section,
    source: 'ehliyet.digital',
    questions: shuffled
  });
};
