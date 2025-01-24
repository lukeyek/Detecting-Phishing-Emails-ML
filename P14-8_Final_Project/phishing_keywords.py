unigrams = {
    'urgent': [
        'action',
        'alert',
        'asap',
        'attention',
        'critical',
        'immediate',
        'immediately'
        'important',
        'importantly',
        'imminent',
        'urgent',
        'urgently'
    ],
    'financial': [
        'account',
        'bank',
        'banking',
        'cash',
        'credit',
        'claim',
        'deposit',
        'fund',
        'funds',
        'investment',
        'loan',
        'money',
        'prize',
        'profit',
        'refund',
        'withdraw',
        'withdrawal',
        'transfer',
        'transaction'
    ],
    'security': [
        'authentication',
        'breach',
        'password',
        'privacy',
        'secure',
        'suspicious',
        'threat',
        'update',
        'verify',
        'verified'
    ],
    'offer': [
        'deal',
        'discount',
        'exclusive',
        'free',
        'giveaway',
        'offer',
        'promotion',
        'trial',
        'voucher'
    ],
    'personal': [
        'beloved',
        'confidential',
        'dear',
        'data',
        'identity',
        'info',
        'personal',
        'private',
        'respected',
        'secret',
        'sensitive'
    ],
    'cta': [
        'act',
        'claim',
        'click',
        'download',
        'help',
        'register',
        'sign',
        'start',
        'subscribe'
    ]
}

bigrams = {
    'urgent': [
        'attention required',
        'critical action',
        'critical issue',
        'critical update',
        'immediate action',
        'immediate attention',
        'immediate response',
        'respond asap',
        'urgent issue',
        'urgent response',
        'urgent action',
        'urgent transfer'
    ],
    'financial': [
        'account update',
        'bank transfer',
        'bank account',
        'cash prize',
        'emergency funds',
        'emergency fund',
        'funds needed',
        'financial assistance',
        'money laundering',
        'refund issued',
        'win prize'
    ],
    'security': [
        'password reset',
        'reset password',
        'security breach',
        'secure your',
        'suspicious activity',
        'update security',
        'update your',
        'unauthorized access',
        'verify account',
        'verify identity'
    ],
    'offer': [
        'claim prize',
        'discount code',
        'exclusive offer',
        'free gift',
        'get paid',
        'limited time',
        'limited offer',
        'special promotion'
    ],
    'personal': [
        'beloved one',
        'confidential data',
        'confidential matter',
        'confidential information',
        'dear friend',
        'identity theft',
        'personal information',
        'secret details',
        'sensitive info'
    ],
    'cta': [
        'claim prize',
        'click here',
        'download now',
        'download document',
        'register now',
        'sign up',
        'subscribe today'
    ]
}

trigrams = {
    'urgent': [
        'action required immediately',
        'action required now',
        'critical issue detected',
        'immediate action needed',
        'immediate action required',
        'immediate response required',
        'important notice immediately',
        'response needed urgently',
        'urgent action required',
        'urgent attention needed',
        'urgent funds needed',
        'urgent funds transfer'
    ],
    'financial': [
        'account balance update',
        'bank account information',
        'claim your refund',
        'earn money from',
        'investment opportunity available',
        'money transfer pending',
        'refund processing now',
        'win cash prize',
        'credit card details'
    ],
    'security': [
        'account security risk',
        'confirm your identity',
        'confirm your password',
        'reset your password',
        'security breach alert',
        'suspicious activity detected',
        'suspicious login attempt',
        'update your account',
        'update your security',
        'verify your account'
    ],
    'offer': [
        'exclusive deal today',
        'just for you',
        'limited time offer',
        'secure your prize',
        'special offer today',
        'special promotion today',
        'your free gift',
        'get exclusive offer',
        'download your discount'
    ],
    'personal': [
        'i need help',
        'identity theft protection',
        'need your assistance',
        'personal data breached',
        'personal data breach',
        'personal information needed',
        'sensitive information required'
    ],
    'cta': [
        'click here to claim',
        'click link below',
        'click link here',
        'download document here',
        'download file here',
        'sign up now',
        'claim reward here'
    ]
}

