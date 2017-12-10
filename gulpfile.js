var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');

var baseSrcDir = 'tracker/static-dev';
var baseDestDir = 'tracker/static';

gulp.task('sass', function () {
    gulp.src(baseSrcDir + '/scss/*.scss')
        .pipe(sass())
        .pipe(gulp.dest(baseSrcDir + '/css'));
});

gulp.task('copy-third-party-styles', function () {
	gulp.src([
		baseSrcDir + '/components/foundation-icon-fonts/foundation-icons.{ttf,woff,eof,svg}',
		baseSrcDir + '/components/select2/dist/css/select2.min.css'
	])
	.pipe(gulp.dest(baseSrcDir + '/css'));
});

gulp.task('build-styles', ['sass', 'copy-third-party-styles'])

gulp.task('concat-js', function() {
	gulp.src([
			baseSrcDir + '/components/fastclick/lib/fastclick.js',
			baseSrcDir + '/components/jquery/dist/jquery.min.js',
			baseSrcDir + '/components/foundation/js/foundation.min.js',
			baseSrcDir + '/components/select2/dist/js/select2.min.js',
			baseSrcDir + '/js/app.js'
		])
		.pipe(concat('app.built.js'))
		.pipe(gulp.dest(baseDestDir + '/js'));
});


gulp.task('copy-styles', function () {
	gulp.src(baseSrcDir + '/css/*.{css,ttf,woff}').pipe(gulp.dest(baseDestDir + '/css/'));
});

gulp.task('copy-js', function () {
	gulp.src(baseSrcDir + '/components/modernizr/modernizr.js').pipe(gulp.dest(baseDestDir + '/js/'));
});

gulp.task('build', ['build-styles', 'copy-styles', 'copy-js', 'concat-js'])
gulp.task('default', ['build-styles']);
