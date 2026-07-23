
document.addEventListener('alpine:init', () => {
  Alpine.data('searchWidget', () => ({
    open: false,
    query: '',
    resultsHtml: '',
    loading: false,
    liveUrl: '',
    resultsUrl: '',

    init() {
      // URLs come from data-* attributes rather than being hardcoded
      // here, so Django's urls.py stays the single source of truth —
      // if a route prefix ever changes, this file doesn't need to.
      this.liveUrl = this.$el.dataset.searchLiveUrl;
      this.resultsUrl = this.$el.dataset.searchResultsUrl;
    },

    toggle() {
      this.open = !this.open;
      if (this.open) this.$nextTick(() => this.$refs.searchInput?.focus());
    },

    close() {
      this.open = false;
    },

    async search() {
      const trimmed = this.query.trim();
      if (trimmed.length < 2) {
        this.resultsHtml = '';
        return;
      }
      this.loading = true;
      try {
        const response = await fetch(`${this.liveUrl}?q=${encodeURIComponent(trimmed)}`);
        if (response.ok) this.resultsHtml = await response.text();
      } catch (err) {
        console.error('Search request failed:', err);
      } finally {
        this.loading = false;
      }
    },

    goToFullResults() {
      const trimmed = this.query.trim();
      if (trimmed) window.location.href = `${this.resultsUrl}?q=${encodeURIComponent(trimmed)}`;
    },
  }));
});