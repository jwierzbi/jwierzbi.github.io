## Generating Pygments CSS files

To generate CSS file with Pygments styles one can use `pygmentize` command:

```shell
pygmentize -S [style_name] -f html -a .highlight > [filename].css
```

The `-a .highlight` option prepends each style definition with `.highlight`
class.

For example for *solarized-light* style:

```shell
pygmentize -S solarized-light -f html -a .highlight > pygments-solarized-light.css
```

## Build the CCS file

```shell
npm run css-build
```
