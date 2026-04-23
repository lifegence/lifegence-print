import * as path from 'path';
import { createOrphanDocTypeSpec } from '@lifegence/e2e-common';
import { KNOWN_UI_HIDDEN_DOCTYPES } from '../../fixtures/coverage-allowlist';

createOrphanDocTypeSpec({
  modules: ['Print Design'],
  appRoot: path.resolve(__dirname, '../../../lifegence_print'),
  entryPoints: ['/desk', '/desk/print-design'],
  allowlist: KNOWN_UI_HIDDEN_DOCTYPES,
});
