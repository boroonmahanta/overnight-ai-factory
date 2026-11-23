# getai-lcp bundle

For low-code project repos: the `getai` and `getai-lcp` presets, the `getai-spec-check` extension, and Spec Kit's `assess` and `bug` extensions. Needs Spec Kit 1.4.3 and `python3` with PyYAML.

Until the private `getai` catalog exists (DG8), install the parts one by one with `--dev`, as `../../README.md` says. After DG8:

```bash
specify bundle install <path>/bundle.yml
```

The lean preset is left out on purpose: its `implement` skips hooks, and so would skip the spec check.
