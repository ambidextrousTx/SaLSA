#################################################################################
# The server must be running in order for this module to work.
#
# The N-Gram Indexer, server, and this client module is implemented by;
# Hakan Ceylan
# hakan@unt.edu
# 2007
#################################################################################

#!/usr/bin/perl -w

use Socket;
use FileHandle;
use strict;

use constant DIGITS_TO_SEND => 4;
use constant MAX_NGRAM => 5;


sub connect()
{
	my( $host, $port, $socket ) = @_;

	my $protocol = 0;
	my $iaddr = inet_aton( $host );
	my $paddr = sockaddr_in( $port, $iaddr );

	socket( $socket, PF_INET, SOCK_STREAM, $protocol ) or die( "Socket: $!" );
	connect( $socket, $paddr ) or die( "Connect: $!" );

	return $socket;
}

sub closeConnection()
{
	my $socket = shift;
	close $socket or die "close: $!";
}

sub send()
{
	my( $socket, $string, $method ) = @_;

	my @chars = split( //, $string );
	my $numOfChars = @chars;

	my $numOfDigits = 0;
	my $lengthString = "";
	while( $numOfChars != 0 )
	{
		$lengthString = ($numOfChars % 10) . $lengthString;
		$numOfChars = int( $numOfChars / 10 );
		$numOfDigits++;
	}

	for( ; $numOfDigits < DIGITS_TO_SEND; $numOfDigits++ )
	{
		$lengthString = "0" . $lengthString;
	}

	#print( "SENDING $method $lengthString $string\n" );
	send( $socket, $method, 0 );
	send( $socket, $lengthString, 0 );
	send( $socket, $string, 0 );
}

sub receive()
{
	my( $socket, $method, $resultsP ) = @_;

	if( $method == 0 )
	{
		my $message = <$socket>;
		chomp( $message );
		return int( $message );
	}
	elsif( $method == 1 )
	{
		my $numOfRecords = <$socket>;
		chomp( $numOfRecords );
		$numOfRecords = int( $numOfRecords );
		for( my $i = 0; $i < $numOfRecords; $i++ )
		{
			my $message = <$socket>;
			chomp( $message );
			push( @{$resultsP}, $message );
			#print( "$message\n" );
		}
	}
	else
	{
		my $message = <$socket>;
		chomp( $message );
		return $message;
	}
}

sub preProcess()
{
	my( $string ) = @_;

	chomp( $string );
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	$string =~ s/\s+/ /g;
	my @tokens = split( /\s+/, $string );
	my $numOfWords = scalar( @tokens );

	if( $numOfWords <= 1 || $numOfWords > ( MAX_NGRAM + 1 ) )
	{
		return 0;
	}

	return $string;
}

sub get()
{
	my( $socket, $string, $method ) = @_;

	if( &preProcess( $string ) )
	{
		&send( $socket, $string, $method );
		return &receive( $socket, $method );
	}

	return 0;
}

sub getNgramCount()
{
	my( $socket, $string ) = @_;

	return &get( $socket, $string, 0 );
}

sub getNgram()
{
	my( $socket, $string, $resultsP ) = @_;

	my $method = 1;
	if( &preProcess( $string ) )
	{
		&send( $socket, $string, $method );
		&receive( $socket, $method, $resultsP );
	}
}

sub getProb()
{
	my( $socket, $string ) = @_;

	return &get( $socket, $string, 2 );
}

sub getAbsDiscountProb()
{
	my( $socket, $string ) = @_;

	return &get( $socket, $string, 3 );
}

sub getKNDiscountProb()
{
	my( $socket, $string ) = @_;

	return &get( $socket, $string, 4 );
}

sub getKNMCDiscountProb()
{
	my( $socket, $string ) = @_;

	return &get( $socket, $string, 5 );
}

sub getDirichletProb()
{
	my( $socket, $string ) = @_;

	return &get( $socket, $string, 6 );
}

sub getDKNProb()
{
	my( $socket, $string ) = @_;

	return &get( $socket, $string, 7 );
}

1;
