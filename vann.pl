#!/usr/bin/perl

sub tocm   {
	return ($_[0] * 100);
}

sub datestring {
	$s = $_[0];
	return substr($s, 0, 2) . "." . substr($s, 2, 2) . "." . substr($s, -4);
}

$norm = 117.69;

system('wget', '-q', 'http://www2.nve.no/h/hd/plotreal/H/0002.00101.000/doegndata.txt');

open(FILE, "<doegndata.txt") || die ("Filen med grunndata finnes ikke, eller kunne ikke åpnes");

my $siste=0;
my $maxh=0.0;
my $maxd=0;
while (<FILE>)   {
	chomp;
	if ( m/^(\d+).*(\d{3}\.\d{4}).*$/ )   {  	# Finn strenger som inneholder måling
		$data[++$siste] = $_;					# Lagre data
		if ($2 > $maxh)   {						# Hent max-verdier
			$maxh = $2;
			$maxd = datestring($1);
		}
	}
}

close(FILE);										# Lukk filen
unlink('doegndata.txt');						# Slett datafilen

# Finn verdier for siste måling
if ($data[$siste] =~ m/^(\d+).*(\d{3}\.\d{4}).*$/)   {
	$sistedato = datestring($1);
	$sistehoyde = $2 - $norm;
}

# Finn verdier for målingen før den siste
if ($data[$siste-1] =~ m/^(\d+).*(\d{3}\.\d{4}).*$/)   {
   $nestsistedato = datestring($1);
   $nestsistehoyde = $2 - $norm;
}

printf("Mjøsa: Siste måling var %s, %0.4f m\n", $sistedato, $sistehoyde);

if ($sistehoyde > $nestsistehoyde)   {
	$diff = tocm($sistehoyde - $nestsistehoyde);
	$hilo = 'høyere';
}
elsif ($sistehoyde < $nestsistehoyde)   {
	$diff = tocm($nestsistehoyde - $sistehoyde);
	$hilo = 'lavere';
}
else   {
	print "Ingen differanse siden siste måling!\n";
	exit(0);
}
printf("%0.2f cm %s enn forrige måling %s\n", $diff, $hilo, $nestsistedato);
printf("Årets høyeste måling var %s på %0.4f m\n", $maxd, ($maxh-$norm));

