import { LitElement, html, css } from 'lit';

class MyElement extends LitElement {
  static styles = css`
    p { color: blue; }
  `;

  constructor() {
    super();
    this.message = 'Loading...';
  }

  connectedCallback() {
    super.connectedCallback();
    fetch('/api/data')
      .then(response => response.json())
      .then(data => this.message = data.message)
      .catch(error => console.error(error));
  }

  render() {
    return html`<p>${this.message}</p>`;
  }
}

customElements.define('my-element', MyElement);
