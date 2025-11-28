export const BibleTranslations = {
    KJV : 'KJV',
    NKJV: 'NKJV',
    RSV : 'RSV',
    NRSV: 'NRSV',
    NASB: 'NASB',
    ESV : 'ESV',
    NET : 'NET',
    NIV : 'NIV',
    NRT : 'NRT',
    RUSV: 'RUSV'
} as const;

export type BibleTranslation = typeof BibleTranslations[keyof typeof BibleTranslations];