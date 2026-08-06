const data = require('../mcp/data/quick-facts.json');

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

  let facts = data;

  if (section !== 'all') {
    const mapped = SECTION_MAP[section];
    if (!mapped) {
      return res.status(400).json({
        error: 'Geçersiz section. Kullanılabilir değerler: ilk_yardim, trafik_ve_cevre, arac_teknigi, trafik_adabi, all'
      });
    }
    facts = data.filter(f => f.section === mapped);
  }

  res.status(200).json({
    count: facts.length,
    section: section,
    source: 'ehliyet.digital',
    facts: facts
  });
};
