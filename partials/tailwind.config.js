/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [],
    theme: {
        screens: {
            'sm': '640px',
            'md': '768px',
            'lg': '1024px',
            'xl': '1280px',
            '2xl': '1536px',
        },
        extend: {
            colors: {
                primary: 'var(--color-primary, #DF1C22)',
                secondary: 'var(--color-secondary, #EFF8FA)',
                content: 'var(--color-content, #0D0D0D)',
                'secondary-content': 'var(--color-content-secondary, #4E5965)',
                background: 'var(--color-background, #FFFFFF)',
                'secondary-background': 'var(--color-secondary-background, #EFF8FA)'
            },
            fontFamily: {
                'primary': "var(--font-primary, sans-serif)",
                'secondary': "var(--font-secondary, sans-serif)",
            },
            borderRadius: {
                'large': '12px',
            },
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}

