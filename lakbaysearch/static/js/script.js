(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {

        const searchForm = document.getElementById('search-form');
        const loadingIndicator = document.getElementById('loading-indicator');
        const searchButton = document.getElementById('search-button');

        if (searchForm && loadingIndicator) {
            searchForm.addEventListener('submit', function () {
                const searchInput = document.getElementById('search-input');
                if (searchInput && searchInput.value.trim() !== '') {
                    loadingIndicator.classList.remove('d-none');
                    if (searchButton) {
                        searchButton.disabled = true;
                    }
                }
            });
        }

        const clearButton = document.getElementById('clear-button');
        const searchInput = document.getElementById('search-input');

        if (clearButton && searchInput) {
            clearButton.addEventListener('click', function () {
                searchInput.value = '';
                searchInput.focus();
            });
        }

        const examplePills = document.querySelectorAll('.example-pill');
        examplePills.forEach(function (pill) {
            pill.addEventListener('click', function () {
                const query = this.getAttribute('data-query');
                if (query && searchInput) {
                    searchInput.value = query;
                    if (searchForm) {
                        if (loadingIndicator) {
                            loadingIndicator.classList.remove('d-none');
                        }
                        if (searchButton) {
                            searchButton.disabled = true;
                        }
                        searchForm.submit();
                    }
                }
            });
        });

        const categoryFilter = document.getElementById('category-filter');
        const sourceFilter = document.getElementById('source-filter');

        function submitWithFilters() {
            if (searchForm) {
                if (loadingIndicator) {
                    loadingIndicator.classList.remove('d-none');
                }
                searchForm.submit();
            }
        }

        if (categoryFilter) {
            categoryFilter.addEventListener('change', function () {
                submitWithFilters();
            });
        }

        if (sourceFilter) {
            sourceFilter.addEventListener('change', function () {
                submitWithFilters();
            });
        }

        document.addEventListener('keydown', function (e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                if (searchInput) {
                    searchInput.focus();
                }
            }
            if (e.key === 'Escape' && searchInput === document.activeElement) {
                if (clearButton) {
                    clearButton.click();
                }
            }
        });

        const resultCards = document.querySelectorAll('.result-card');
        if (resultCards.length > 0 && 'IntersectionObserver' in window) {
            const observer = new IntersectionObserver(
                function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translateY(0)';
                            observer.unobserve(entry.target);
                        }
                    });
                },
                { threshold: 0.1 }
            );

            resultCards.forEach(function (card) {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                observer.observe(card);
            });
        }

        const statCards = document.querySelectorAll('.stat-card');
        if (statCards.length > 0 && 'IntersectionObserver' in window) {
            const observer = new IntersectionObserver(
                function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translateY(0)';
                            observer.unobserve(entry.target);
                        }
                    });
                },
                { threshold: 0.1 }
            );

            statCards.forEach(function (card) {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                observer.observe(card);
            });
        }

        const glassCards = document.querySelectorAll('.glass-card');
        if (glassCards.length > 0 && 'IntersectionObserver' in window) {
            const observer = new IntersectionObserver(
                function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translateY(0)';
                            observer.unobserve(entry.target);
                        }
                    });
                },
                { threshold: 0.1 }
            );

            glassCards.forEach(function (card) {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                observer.observe(card);
            });
        }
    });

})();