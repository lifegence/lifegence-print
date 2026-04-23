import { createLegacyRedirectSpec } from '@lifegence/e2e-common';

createLegacyRedirectSpec({
  paths: [
    { legacy: '/app/print-design', canonical: '/desk/print-design' },
    { legacy: '/app/print-template-jp', canonical: '/desk/print-template-jp' },
  ],
});
