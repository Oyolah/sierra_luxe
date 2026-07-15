/**
 * Sierra Luxe - Theme Controller
 * Handles Light Mode and Dark Mode switching with localStorage persistence
 */

const ThemeController = (function() {
    const THEME_STORAGE_KEY = 'sierra_luxe_theme';
    const THEME_ATTRIBUTE = 'data-theme';
    const THEMES = {
        LIGHT: 'light',
        DARK: 'dark'
    };

    /**
     * Get the current theme from localStorage
     * @returns {string} Current theme ('light' or 'dark')
     */
    function getStoredTheme() {
        try {
            const stored = localStorage.getItem(THEME_STORAGE_KEY);
            return stored && (stored === THEMES.LIGHT || stored === THEMES.DARK) 
                ? stored 
                : THEMES.LIGHT; // Default to light mode
        } catch (e) {
            console.warn('Error reading theme from localStorage:', e);
            return THEMES.LIGHT;
        }
    }

    /**
     * Save theme to localStorage
     * @param {string} theme - Theme to save ('light' or 'dark')
     */
    function saveTheme(theme) {
        try {
            localStorage.setItem(THEME_STORAGE_KEY, theme);
        } catch (e) {
            console.warn('Error saving theme to localStorage:', e);
        }
    }

    /**
     * Apply theme to document
     * @param {string} theme - Theme to apply ('light' or 'dark')
     */
    function applyTheme(theme) {
        if (theme === THEMES.DARK) {
            document.documentElement.setAttribute(THEME_ATTRIBUTE, THEMES.DARK);
        } else {
            document.documentElement.removeAttribute(THEME_ATTRIBUTE);
        }
    }

    /**
     * Get the current applied theme
     * @returns {string} Current theme ('light' or 'dark')
     */
    function getCurrentTheme() {
        return document.documentElement.hasAttribute(THEME_ATTRIBUTE) 
            ? THEMES.DARK 
            : THEMES.LIGHT;
    }

    /**
     * Toggle between light and dark mode
     */
    function toggleTheme() {
        const currentTheme = getCurrentTheme();
        const newTheme = currentTheme === THEMES.LIGHT ? THEMES.DARK : THEMES.LIGHT;
        
        applyTheme(newTheme);
        saveTheme(newTheme);
        updateThemeIcons(newTheme);
        
        // Dispatch custom event for other components to listen to
        document.dispatchEvent(new CustomEvent('themeChanged', { 
            detail: { theme: newTheme } 
        }));
    }

    /**
     * Update all theme toggle icons on the page
     * @param {string} theme - Current theme ('light' or 'dark')
     */
    function updateThemeIcons(theme) {
        const icons = document.querySelectorAll('.theme-toggle-icon');
        icons.forEach(icon => {
            if (theme === THEMES.DARK) {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            } else {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            }
        });

        // Update button text if present
        const buttons = document.querySelectorAll('.theme-toggle-text');
        buttons.forEach(text => {
            text.textContent = theme === THEMES.DARK ? 'Dark Mode' : 'Light Mode';
        });
    }

    /**
     * Initialize theme system
     * This should be called as early as possible to prevent theme flashing
     */
    function init() {
        const storedTheme = getStoredTheme();
        applyTheme(storedTheme);
        
        // Remove loading class if present
        document.body.classList.remove('theme-loading');
        
        // Update icons after DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                updateThemeIcons(storedTheme);
                attachEventListeners();
            });
        } else {
            updateThemeIcons(storedTheme);
            attachEventListeners();
        }
    }

    /**
     * Attach event listeners to theme toggle buttons
     */
    function attachEventListeners() {
        const toggles = document.querySelectorAll('.theme-toggle');
        toggles.forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                toggleTheme();
            });
        });
    }

    /**
     * Public API
     */
    return {
        init: init,
        toggle: toggleTheme,
        getCurrentTheme: getCurrentTheme,
        applyTheme: applyTheme,
        THEMES: THEMES
    };
})();

// Auto-initialize when script loads
ThemeController.init();
