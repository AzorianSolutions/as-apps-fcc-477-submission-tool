# Requirements

## Python Libraries

You should **install the latest** Geocod.io Python library which can be found here:
https://github.com/bennylope/pygeocodio.

**The version installed by some IDEs are not up-to-date enough to support the functions used in this app.**

> pip3 install pygeocodio

## Geocod.io API Key

You will need an API key for a Geocod.io account that has enough credits to support your requests.

Once signed in to your Geocod.io account, navigate to this page for an API key: https://dash.geocod.io/apikey

**REMEMBER!** When creating the API key, ensure that it has been granted the "POST /v1.7/geocode" permission for batch
geocoding.

## Permissions

Ensure that the tool.py file has executable permissions. If you're on a Linux machine, you can achieve that most easily
with the following command:

> chmod +x ./tool.py

# Using The Tool

This tool has two primary modes of operation currently. Each mode is detailed below with associated CLI arguments to
configure the app.

At this time, the tool is specifically designed to deal with submissions for transmission technology 70
(Terrestrial Fixed Wireless). So this means small to medium WISP operators may find this very useful.

Depending on feedback to the project repository, I will consider introducing support to handle hybrid submissions to
include transmission technology 50 (Optical Carrier).

## Non-Standard CSV Formats

If you're dealing with a scenario that is less than standard with your CSV files, you can also override the delimiter
and quoting character settings with the following arguments:

-D ( --delimiter ): The delimiter to use for reading source CSV files. Defaults to the comma character ( , )

-q ( --quote ): The quoting character to use when reading source CSV files. Defaults to the double quote character ( " )

Example:

> ./tool.py -m bd -s ./FCCData.csv -t ./deployment.csv -D '|' -q '`'

## Broadband Deployment Data

### Overview

As this time, the broadband deployment mode is designed to process the "FCCData.csv" file that is currently generated
from the "Fixed Broadband Deployment Data for FCC Form 477" service provided by https://towercoverage.com. The CSV file
provided by this service does not come in a format that is valid for direct submission to the FCC.

This tool can help bridge that gap provided your reporting scenario meets the following criteria:
1. The highest consumer broadband speed plan you offer is available in all the Census blocks included in this processing.
2. You either do or don't offer consumer broadband service in all the Census blocks included in this processing.
3. You either do or don't offer business / government broadband service in all the Census blocks included in this processing.

Simply put, it would take a lot of work to create a valuable feature for handling anything more advanced than this. It
should be sufficient for a large number of operators though.

### TLDR

To run the tool in this mode, the following are the minimum arguments you must define to get started:

-m ( --mode ): The app mode run, in this scenario you should use "bd".

-s ( --source ): The source CSV file to mutate data from.

-t ( --target ): The target CSV file to save the mutated data into.

Example:

To run an interactive process of a TowerCoverage deployment data export using all defaults, execute
something like the following:

> ./tool.py -m bd -s ./FCCData.csv -t ./deployment.csv

### Non-Interactive Mode

There are four configuration options that are normally collected through interactive mode. These options can be provided
at runtime via CLI arguments which are as follows:

-c ( --consumer ): If consumer broadband service is available in all Census blocks then yes, no otherwise.

-b ( --business ): If business / government broadband service is available in all Census blocks then yes, no otherwise.

-d ( --downstream ): Maximum consumer broadband downstream plan speed advertised in all Census blocks (Mbps)

-u ( --upstream ): Maximum consumer broadband upstream plan speed advertised in all Census blocks (Mbps)

Example:

This example assumes you offer both consumer and business / government broadband service in all included Census blocks with a
maximum advertised speed plan of 75 Mbps downstream and 15 Mbps upstream.

> ./tool.py -m bd -s ./FCCData.csv -t ./deployment.csv -c y -b y -d 75 -u 15

For more information on what these options mean, check out the "Fixed Broadband Deployment Formatting" guide which can be
found here: https://us-fcc.app.box.com/v/FBDFormatting

## Broadband Subscription Data

### Overview

At this time, the broadband subscription mode is designed to handle a fairly wide range of scenarios that involve CSV
data as the mutation source. One example of this, is if you're using Quickbooks for tracking your customer speed plans.
Another example could be a simple custom report in Powercode. Depending on what version of the platform you run, you may
have found the built-in 477 export feature to be unstable. This tool can yet again bridge that gap.

Consider a messy scenario where the only Quickbooks report I can create to provide the data needed, results in bloat
rows for each customer record exported. That's not a problem here since this process is designed to automatically skip
rows that don't contain values in the configured street, city, state, and zip columns.

Continuing with the aforementioned scenario, what about when the order of columns in the source CSV file
are not correct? Even worse, consider a scenario where there are additional columns that you don't need. Sure, you can
manage column ordering and padding issues fairly easy in any typical desktop spreadsheet application today. Do you
really want to do this tedious, at-risk step every time?

Why bother regardless, I just solved that problem for you! See additional information below regarding the
-o ( --order ) argument.

### TLDR

To run the tool in this mode, the following are the minimum arguments you must define to get started:

#### -m ( --mode )
The app mode run, in this scenario you should use "bs".

#### -s ( --source )
The source CSV file to mutate data from.

#### -t ( --target )
The target CSV file to save the mutated data into.

#### -k ( --apikey )
The Geocod.io API key with POST /v1.7/geocode permissions for an account with enough credits and daily limit allowance
to fulfill the desired request.

#### Example:

To process a Quickbooks Desktop report CSV export, execute something like the following:

> ./tool.py -m bs -s ./quickbooks-report.csv -t ./subscription.csv -k API-KEY-HERE &#92; \
> &nbsp;&nbsp;&nbsp;&nbsp;-w y -S 1 -a y -o none,none,street,none,city,state,zip,aux

I realize there is a lot going on in this command so **it would be prudent** to read the next section for
"Additional Arguments".

### Additional Arguments

#### -w ( --warn )
Whether to give a warning in the console for each row missing required values. Valid values are 'yes', 'y', '1', 'no',
'n', and '0'.

**@Default**: no

#### -S ( --skip )
How many rows to skip from the beginning of the source CSV file when consuming the CSV data.

**@Default**: 0

#### -o ( --order )
The order which columns are defined in the source CSV file. Each column that provides relevant input to the app has been
assigned a static reference of sorts which is as follows:

> street, city, state, zip, ds, dsu, us, usu, aux, none

**@Default**: street,city,state,zip,ds,dsu,us,usu,aux

The first four columns should be pretty self-explanatory. The next four are fairly simple, but the last couple, not so
much.

**ds**: Downstream Bandwidth

This column should contain either a float or integer value representing the highest download speed advertised on the
subscriber's speed plan.

**dsu**: Downstream Bandwidth Unit

The unit of measure for the value in the **ds** column. This can be of 'k' for Kbps, 'm' for Mbps, or 'g' for Gbps.

**us**: Upstream Bandwidth

This column should contain either a float or integer value representing the highest upload speed advertised on the
subscriber's speed plan.

**usu**: Upstream Bandwidth Unit

The unit of measure for the value in the **us** column. This can be of 'k' for Kbps, 'm' for Mbps, or 'g' for Gbps.

**aux**: Auxiliary Data Column

This column is typically only used in conjunction with the -a ( --aux ) argument. Refer to the arguments documentation
below.

**none**: None

This column label is special in that you can use it multiple times to act as a placeholder for other columns in your
source CSV file that aren't relevant.

For example, let's say you have a source CSV file that has the following columns of data contained within in this order;

> Subscriber Name, Organization Name, Street Address 1, Street Address 2, City, State, Zip, Download Speed, Download
> Speed Unit, Upload Speed, Upload Speed Unit

You would want to define the -o ( --order ) argument like this:

> ./tool.py -m bs -s ./quickbooks-report.csv -t ./subscription.csv -k API-KEY-HERE &#92; \
> &nbsp;&nbsp;&nbsp;&nbsp;-o none,none,street,none,city,state,zip,ds,dsu,us,usu

#### -a ( --aux )
Whether to enable the use of the auxiliary speed extraction feature. Valid values are 'yes', 'y', '1', 'no',
'n', and '0'.

**@Default**: no

#### -r ( --regex )
The regular expression to use for the auxiliary speed extraction feature. Refer to the "Auxiliary Speed Extraction
Feature" section below for additional information.

**@Default**:

> ([0-9]{1,3})(?:\.([0-9]{1,2}))?([kmg])?(?:/?([0-9]{1,3})(?:\.([0-9]{1,2}))?([kmg])?)?

### Headers / Skipping Rows

Headers aren't needed by this app so you can either leave them out of your source CSV file or you can make use of the -S
( --skip ) argument to skip a given number of rows from the beginning of the source CSV file. Refer to the "Additional
Arguments" section above for additional information on the -S ( --skip ) argument. 

### Custom Column Ordering

Refer to the "Additional Arguments" section above, specifically the -o ( --order ) argument for examples on dealing with column re-ordering.

### Auxiliary Speed Extraction Feature

This app has a feature that was designed to deal with complicated source CSV data scenarios like Quickbooks where
subscriber speed plan information may be mixed in to a shared text field containing other data. This feature may be
activated by setting the -a ( --aux ) argument to 'yes', 'y', or 1.

This feature works by applying a regular expression to the value of the aux column to extract six individual pieces of
data through the use of six capture groups. The six capture groups should be as follows with strict adherence to the
order:

1. Downstream Speed (left of decimal if any)
2. Downstream Speed (right of decimal if any)
3. Downstream Speed Unit (should seek one of 'k', 'm', or 'g')
4. Upstream Speed (left of decimal if any)
5. Upstream Speed (right of decimal if any)
6. Upstream Speed Unit (should seek one of 'k', 'm', or 'g')

Refer to the "Additional Arguments" section above, specifically to the -r ( --regex ) argument for additional
information.

##  Voice Subscription Data

**NOT SUPPORTED**

There is currently no built-in support for processing voice subscription data. If you want to fund the development with
appropriate donations, I will consider an offer to develop this functionality to support your use case.
