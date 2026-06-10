Team,

Lakehouse has been live for two weeks - here are the updates:


TL;DR
----------
1. Half-hourly plant should now be read from the Lakehouse tables
2. From mid-July all forecast tables will be in Lakehouse tables
3. From mid-August half-hourly data will only be available in Lakehouse tables


Lakehouse is just new tables
----------
Lakehouse is a totally new platform that will scale with Aurora's growing data needs. However, to minimise disruption, we're making
Lakehouse tables available through the old Data Warehouse.

This means using Lakehouse is as simple as connecting to the DataWarehouse and using new tables.

Lakehouse tables have the form _origin_bronze.halfhourlyplant_ and by mid-July we'll have tables for each model output.


Downsizing DataWarehouse
----------
In early August we'll drop all of the old DataWarehouse half-hourly tables. From this point you'll need to use new Lakehouse tables.

Please be in touch if you have any concerns or need any support.

Goodies and updates
----------
* Lakehouse now has [currency views](https://auroraenergy.atlassian.net/wiki/spaces/DA/pages/6588170581/2026-06-09+Silver+tables+Athena+and+more#How-do-we-get-Lakehouse-data-in-a-specific-currency%2C-or-inflated-to-a-specific-year%3F)
* We have an [Athena dashboard dedicated to Half-Hourly Plant](https://auroraenergy.atlassian.net/wiki/spaces/DA/pages/6588170581/2026-06-09+Silver+tables+Athena+and+more#What-is-new-in-Athena%3F) (kudos @matteo tabaro)
* Please use [Data Warehouse Dimension tables](https://auroraenergy.atlassian.net/wiki/spaces/DA/pages/6588170581/2026-06-09+Silver+tables+Athena+and+more#Continue-using-Data-Warehouse-dimension-tables)


See something, say something
----------
We're pushing Lakehouse aggressively because it's the only way to avoid the issues caused by the Warehouse in April.

Because we're moving fast there may be a few small bumps: apologies in advance if this is the case! Thanks in to those of your who've already flagged issues for us - please keep this up :thumb.

You can contact us in [DataHub](https://teams.microsoft.com/l/channel/19%3Ad21d85dab2e94b5092ca87e6762695df%40thread.skype/Data%20Hub?groupId=9909a8bc-967e-4b37-a58c-eee55e4c836f&tenantId=ad3c7c7d-fe68-4eb7-a656-36bf93cf1d09) or by email - and we're happy to jump on call anytime.



Our next update will be in early July.


Joe
