from pathlib import Path
import json,csv
out=Path(__file__).resolve().parent
S={
'I01':('Zurich EV product','https://www.zurich.co.id/produk-asuransi/untuk-kendaraan/zurich-syariah-ev-autocillin','turn958708782view0','official product page','live retrieved; undated'),
'I02':('Zurich EV RIPLAY','https://www.zurich.co.id/-/media-assets/project/zurich-headless/indonesia/docs/produk/autocillin-syariah/riplay-umum_zurich-syariah-ev-autocillin.pdf','turn184414567view0','official product summary PDF','printed2026-08-07; not full policy'),
'I03':('Astra Syariah','https://www.asuransiastra.com/syariah/','turn874786437search1','official indexed page','directwebopen403; search text available'),
'I04':('Garda Oto','https://www.asuransiastra.com/garda-oto/','turn755250131view2','official product page','opened thenlaterweb403'),
'I05':('Astra myGarda EV','https://www.asuransiastra.com/official-press-release/pengalaman-berasuransi-semakin-mudah-berkat-mygarda-sambut-usia-tujuh-dekade-asuransi-astra-luncurkan-inovasi-terbaru/','turn755250131view3','official release','2026-09-16'),
'I06':('Jasindo Syariah motor','https://www.jasindosyariah.co.id/product/ritel/asuransi-kendaraan-bermotor','turn958708782view2','official product page','undated'),
'I07':('Jasindo claim process','https://www.jasindosyariah.co.id/pages/asuransi-kendaraan-bermotor','turn228076214search1','official indexed process','undated'),
'I08':('Hyundai RVG','https://www.hyundai.com/id/id/myhyundaicare/jual-kembali/resale-value-guarantee','turn184414567view2','official programme terms','undated currentpage'),
'I09':('VinFast GIIAS2026','https://vinfastauto.id/en/promo-giias-2026','turn958708782view4','official campaign','GIIAS2026; detailedtenor not shown'),
'I10':('RVI Group overview','https://www.rvigroup.com/residual-value-insurance/','turn958708782view5','official insurer product','undated; generic international'),
'I11':('RVI passenger','https://www.rvigroup.com/passenger-vehicle/','turn958708782view6','official insurer product','undated; bespoke B2B'),
'I12':('POJK8/2024','https://ojk.go.id/id/regulasi/Documents/Pages/POJK-8-Tahun-2024-Produk-Asuransi-dan-Saluran-Pemasaran-Produk-Asuransi/POJK%208%20Tahun%202024%20Produk%20Asuransi%20dan%20Saluran%20Pemasaran%20Produk%20Asuransi.pdf','turn511683724view1','primary regulation PDF','2024 publication; currentfulllegalposition notcertified'),
'I13':('SEOJK14/2024','https://ojk.go.id/id/regulasi/Pages/SEOJK-14-SEOJK05-2024-Persetujuan-dan-Pelaporan-Produk-Asuransi.aspx','turn228076214search4','official regulation landing','2024-10-29'),
'I14':('DSN fatwa directory','https://dsnmui.or.id/kategori/fatwa/page/12/','turn511683724view0','official DSN directory','lists52and53/2006'),
'I15':('Fatwa52/2006','https://aasi.or.id/storage/regulation-files/v2IwRXT58TZo9Y4cJQ0DndBpEXviMyVcQTOjysn2.pdf','turn237141222view1','original DSN document hostedbyAASI','2006'),
'I16':('IFRS17 historical consolidatedtext','https://www.ifrs.org/content/dam/ifrs/project/amendments-to-ifrs-17/ifrs-17-incorporating-the-june-2020-amendments.pdf','turn237141222view0','standardsetter PDF','2020 consolidation; not currentIndonesialegalopinion'),
'I17':('POJK27/2025','https://ojk.go.id/id/regulasi/Pages/POJK-27-Tahun-2025-Pengelolaan-Aset-dan-Liabilitas-Perusahaan-Asuransi-dan-Perusahaan-Reasuransi-dengan-Prinsip-Syariah.aspx','turn511683724search5','official regulatory landing','2025-11-24 metadata'),
'I18':('AAUI oldlink','https://aaui.or.id/wp-content/uploads/2022/03/11-PSAKBI-rev-dispute-2021.pdf','turn755250131view1','unavailableprimaryPDF','web404; no substance adopted'),
}
rows=[]
def a(sid,locator,friendclaim,finding,status,consequence):
 s=S[sid];rows.append(dict(claim_id=f'INS-{len(rows)+1:03}',source_id=sid,source_url=s[1],retrieval_ref=s[2],source_type=s[3],source_date_scope=s[4],retrieved_date='2026-11-11',document_locator=locator,friend_claim_tested=friendclaim,scoped_finding=finding,verification_status=status,research_implication=consequence,causal_or_commercial_effect='not measured'))
a('I01','package table/FAQ','EVsyariah productexists','Zurich publicly offers EV-specific syariah motor protection.','confirmed_operator_publication','Not a novel product category; dealer connection/demand remain unknown.')
a('I02','PDFp1; physicalpage1','HEV/PHEV/BEV transfer','Object specifies four-wheel battery-electric vehicles.','narrowed','Do not assume this product automatically covers hybrids.')
a('I02','PDFp11 benefit table','charging coverunlimited','Total package: charging battery/vehicle eachRp100m/year; chargerRp20m/year.','narrowed','Full selectedpolicy governs; sums insured are not dealer income.')
a('I02','PDFp10 package table','flood alwaysincluded','Flood included in Total; optional in Custom.','narrowed','Compare selectedpackage, not brandheadline.')
a('I02','PDFp10 package table','automatic authorizeddealer repair','ATPMworkshop benefit is optional in comprehensive packages.','notestablished_asautomatic','Auto2000routing needs actual insurer/workshop eligibility.')
a('I02','PDFp12 riskself table','customerpaysnothing','Batteryfire deductible5%; flood10%minimumRp500k.','narrowed','Residual customerburden remains.')
a('I02','PDFp4 exclusions','normaldegradation covered','Wear, intrinsicmaterialdefect and misuse exclusions are stated.','notestablished_forcapacitydecline','Do not equate accidentalbatteryprotection with SOHwarranty.')
a('I02','PDFp5–6 claimprocess','newclaimapp needed','AMC already handles claim reporting, validation and repairauthorization.','existingcapability_confirmed','Specific incrementalcontinuity value must be demonstrated.')
a('I02','PDFp2 fees','dealercommissionknown','Contribution includes acquisitioncosts; no Auto2000feeshare specified.','commission_unconfirmed','Insurerujrah/acquisitioncost is not verified dealercommission.')
a('I02','PDFp13 akad','tabarrucoversanydealerloss','Fund use and insurerfees follow stated insurancecontract.','notestablished_forRVI','Naming an akad does not create residualvaluecoverage.')
a('I03','productdescription','AstraSyariah feasiblecurrentpartner','Astra describes syariah motor/GardaOto products with distinct contractwording.','confirmed_indexed_operatorclaim','No verified matchingEVbatteryendorsement or signedDigiroomagreement.')
a('I04','cover/exclusion/claimsections','comprehensive meansallloss','Garda distinguishes partial/totalloss and excludes reducedprice/financialloss under statedstandardterms.','narrowed','Ordinarymotorcover is not confirmed depreciationinsurance.')
a('I04','myGarda andclaimprocedure','claimcoordinationnew','Garda already offers claims/survey/SPK andrepairchannels.','existingcapability_confirmed','Assess additionaljobvalue before proposingduplicateclaimworkflow.')
a('I05','release2026-09-16','EVevacuation exists','Astra announces myGarda and updatedGardaSiaga services.','operatorrelease_confirmed','Availability is not proof of model-specific battery/charging cover.')
a('I06','benefits/exclusions','Jasindo motorcoverage','Comprehensive/TLO, optionalflood and naturel-of-object exclusions are described.','confirmed_operatorpublication','No explicit residualprice-loss benefit was identified on this page.')
a('I07','claimprocess','claims onlybooking','Jasindo specifies notice/documents andinsurerinvestigation before repair.','confirmed_indexed_operatorprocess','Scheduling is separate from claimapproval.')
a('I08','terms1–3','Hyundai70percent broadEVprecedent','70%tradein inmonths25–36 applies to namedStargazer/Creta variants.','narrowed','Not a verified HyundaiBEV floor or insurerbacking.')
a('I08','terms7–10','manufacturerfloorunconditional','Originalownership, max60k, officialservice and condition/document rules apply.','narrowed','Eligibility and validredemption matter; absenceofnamedinsurer proves no fundingstructure.')
a('I09','GIIAS2026 benefits','VinFast80percent','Officialcampaign advertises up-to80%resaleguarantee subjecttoterms.','headline_confirmed_detailunresolved','No verified tenor, settlementbasis or insurance-backed structure here.')
a('I10','productoverview','RVIexistsinternationally','Insurer describes future-value coverage for properlymaintained assets.','internationalprecedent_confirmed','Does not verify availability or licensure for an Indonesian customer.')
a('I11','passengervehicleproduct','RVIready-madeconsumeraddon','RVI describes custom policies for banks, financecompanies, lessors andfleets.','narrowed_B2Bprecedent','No published Indonesian syariah quote or automaticdealereligibility.')
a('I12','Art3;PDFp5','anyriskinsurable','Publishedrule requires insurablerisk and appropriatecontribution.','document_requirement_confirmed','No conclusion that proposed puremarketdepreciation is accepted.')
a('I12','Art48–50,53,55;PDFpp25–27','digitaldealer canjustsell','Marketingchannels, writtenagreements and accurate remoteinformation are regulated.','document_requirement_confirmed','Actual arrangement needs insurer/regulatoryassessment; no blanket legality opinion.')
a('I12','Art63;PDFpp30–31','fatwasautomaticallyapproveRVI','Sharia product requires relevantfatwa/basis and DPSopinion on actualproduct/risk/contract.','document_requirement_confirmed','Existing generalfatwas are not product-specific approval.')
a('I13','officialsummary','RVIregulatoryroute alreadysettled','SEOJK14/2024 sets productapproval/reporting and DPSopinion procedures.','framework_confirmed','The specific productroute is unresolved.')
a('I14','fatwatable52/53','fatwas52and53 exist','DSNdirectory lists insurancewakalah andtabarrufatwas.','existence_confirmed','Directory existence alone proves no productapproval.')
a('I15','title;decisionsframework','wakalahfee fixesdealerreward','Fatwa52addresses participantauthority to insurer withujrah.','framework_confirmed','It does not establish a specific dealercommission agreement.')
a('I16','paragraph7(d);AppendixB7–B9','accountingrulesproveinsuranceavailable','IFRS17 excludes certain manufacturer/dealer residualguarantees from its scope.','classification_boundary','Accounting classification is not Indonesian authorization or shariacertification.')
a('I17','officialregulationmetadata','only2024 frameworkmatters','OJK lists2025syariah asset/liability rule covering relatedfundmanagement.','additionalframework_identified','No exhaustive legalcurrency or compliance conclusion.')
with (out/'claim_matrix.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'claim_matrix.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));sources=[dict(source_id=k,title=v[0],url=v[1],retrieval_ref=v[2],type=v[3],scope=v[4]) for k,v in S.items()];(out/'sources.json').write_text(json.dumps(sources,indent=2))
print('claims',len(rows),'sourcecatalog',len(sources),'usedsources',len(set(r['source_id'] for r in rows)))
