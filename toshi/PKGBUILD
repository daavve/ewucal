# Maintainer: David McInnis <davidm@eagles.ewu.edu>

pkgname=toshi-segment
pkgver=3.0
pkgrel=1
pkgdesc="Program from Toshis master's thesis"
arch=('x86_64' 'i686')
url='http://davehub.net'
license=('LGPL3')
makedepends=('opencv2' 'gcc' 'make')
source=("toshi.tar.gz")
sha256sums=('797f055495789effc4c12281ac486b0de5dc63b8fe5a02dcd22b71a6615024f3')

build() {
  cd "${srcdir}"
  make
}

package() {
  cd "${srcdir}"
  install -D -m755 toshi-segment $pkgdir/usr/bin/toshi-segment
}
