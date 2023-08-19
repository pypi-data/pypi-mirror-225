from endesive.pdf import cms
from endesive.pdf.PyPDF2 import pdf, generic as po


class SignedData(cms.SignedData):
    def makepdf(self, prev, udct, algomd, zeros, cert, **params):
        catalog = prev.trailer["/Root"]
        size = prev.trailer["/Size"]
        pages = catalog["/Pages"].getObject()
        page0ref = prev.getPage(udct.get("sigpage", 0)).indirectRef

        self._objects = []
        while len(self._objects) < size - 1:
            self._objects.append(None)

        # if params['mode'] == 'timestamp':
        # deal with extensions
        if "/Extensions" not in catalog:
            extensions = po.DictionaryObject()
        else:
            extensions = catalog["/Extensions"]

        if "/ESIC" not in extensions:
            extensions.update(
                {
                    po.NameObject("/ESIC"): po.DictionaryObject(
                        {
                            po.NameObject("/BaseVersion"): po.NameObject("/1.7"),
                            po.NameObject("/ExtensionLevel"): po.NumberObject(1),
                        }
                    )
                }
            )
            catalog.update({po.NameObject("/Extensions"): extensions})
        else:
            esic = extensions["/ESIC"]
            major, minor = esic["/BaseVersion"].lstrip("/").split(".")
            if int(major) < 1 or int(minor) < 7:
                esic.update(
                    {
                        po.NameObject("/BaseVersion"): po.NameObject("/1.7"),
                        po.NameObject("/ExtensionLevel"): po.NumberObject(1),
                    }
                )

        # obj12 is the digital signature
        obj12, obj12ref = self._make_signature(
            Type=po.NameObject("/Sig"),
            # SubFilter=po.NameObject("/ETSI.CAdES.detached"),
            SubFilter=po.NameObject("/adbe.pkcs7.detached"),
            Contents=cms.UnencryptedBytes(zeros),
        )

        obj12.update(
            {
                po.NameObject("/Prop_Build"): pdf.DictionaryObject(
                    {
                        po.NameObject("/App"): pdf.DictionaryObject(
                            {
                                po.NameObject("/Name"): po.NameObject(
                                    "/" + udct.get("application", "endesive")
                                )
                            }
                        ),
                    }
                ),
            }
        )
        if params["mode"] == "timestamp":
            # obj12 is a timestamp this time
            obj12.update(
                {
                    po.NameObject("/Type"): po.NameObject("/DocTimeStamp"),
                    po.NameObject("/SubFilter"): po.NameObject("/ETSI.RFC3161"),
                    po.NameObject("/V"): po.NumberObject(0),
                }
            )
        else:
            obj12.update(
                {
                    po.NameObject("/Name"): po.createStringObject(udct["contact"]),
                    po.NameObject("/Location"): po.createStringObject(udct["location"]),
                    po.NameObject("/Reason"): po.createStringObject(udct["reason"]),
                }
            )
            if params.get("use_signingdate"):
                obj12.update(
                    {po.NameObject("/M"): po.createStringObject(udct["signingdate"])}
                )

        # obj13 is a combined AcroForm Sig field with Widget annotation
        new_13 = True
        # obj13 = po.DictionaryObject()
        if udct.get("signform", False):
            # Attaching signature to existing field in AcroForm
            if "/AcroForm" in catalog:
                form = catalog["/AcroForm"].getObject()
                if "/Fields" in form:
                    fields = form["/Fields"].getObject()
                    obj13ref = [
                        f
                        for f in fields
                        if f.getObject()["/T"] == udct.get("sigfield", "Signature1")
                    ][0]
                    obj13 = obj13ref.getObject()
                    self._objects[obj13ref.idnum - 1] = obj13
                    new_13 = False

        # box is coordinates of the annotation to fill
        box = udct.get("signaturebox", None)

        if new_13:
            obj13, obj13ref = self._make_sig_annotation(
                F=po.NumberObject(udct.get("sigflagsft", 132)),
                T=cms.EncodedString(udct.get("sigfield", "Signature1")),
                Vref=obj12ref,
                Pref=page0ref,
            )
        else:
            # original obj13 is a merged SigField/SigAnnot
            # Setting /V on the AcroForm field sets the signature
            # for the field
            obj13.update({po.NameObject("/V"): obj12ref})
            # fill the existing signature field annotation,
            # ignore any other location
            if "/Rect" in obj13:
                box = [float(f) for f in obj13["/Rect"]]

        # add an annotation if there is a field to fill
        if box is not None:
            self.addAnnotation(cert, udct, box, page0ref, obj13, obj13ref, new_13)

        if udct.get("sigandcertify", False) and "/Perms" not in catalog:
            obj10 = po.DictionaryObject()
            obj10ref = self._addObject(obj10)
            obj11 = po.DictionaryObject()
            obj11ref = self._addObject(obj11)
            obj14 = po.DictionaryObject()
            obj14ref = self._addObject(obj14)
            obj14.update({po.NameObject("/DocMDP"): obj12ref})
            obj10.update(
                {
                    po.NameObject("/Type"): po.NameObject("/TransformParams"),
                    po.NameObject("/P"): po.NumberObject(udct.get("sigflags", 3)),
                    po.NameObject("/V"): po.NameObject("/1.2"),
                }
            )
            obj11.update(
                {
                    po.NameObject("/Type"): po.NameObject("/SigRef"),
                    po.NameObject("/TransformMethod"): po.NameObject("/DocMDP"),
                    po.NameObject("/DigestMethod"): po.NameObject("/" + algomd.upper()),
                    po.NameObject("/TransformParams"): obj10ref,
                }
            )
            obj12[po.NameObject("/Reference")] = po.ArrayObject([obj11ref])
            catalog[po.NameObject("/Perms")] = obj14ref

        if "/AcroForm" in catalog:
            form = catalog["/AcroForm"].getObject()
            if "/Fields" in form:
                fields = form["/Fields"]
                old_field_names = [f.getObject()["/T"] for f in fields]
            else:
                fields = po.ArrayObject()
                old_field_names = []
            if udct.get("auto_sigfield", False) and obj13["/T"] in old_field_names:
                name_base = udct.get("sigfield", "Signature1")
                checklist = [
                    f[len(name_base) :]
                    for f in old_field_names
                    if f.startswith(name_base)
                ]
                for i in range(1, len(checklist) + 1):
                    suffix = "_{}".format(i)
                    if suffix in checklist:
                        continue

                    new_name = "{}{}".format(name_base, suffix)
                    obj13.update({po.NameObject("/T"): EncodedString(new_name)})
                    break

            old_flags = int(form.get("/SigFlags", 0))
            new_flags = int(form.get("/SigFlags", 0)) | udct.get("sigflags", 3)
            if new_13:
                fields.append(obj13ref)
                form.update(
                    {
                        po.NameObject("/Fields"): fields,
                        po.NameObject("/SigFlags"): po.NumberObject(new_flags),
                    }
                )
            elif new_flags > old_flags:
                form.update({po.NameObject("/SigFlags"): po.NumberObject(new_flags)})
            formref = catalog.raw_get("/AcroForm")
            if isinstance(formref, po.IndirectObject):
                self._objects[formref.idnum - 1] = form
                form = formref
        else:
            form = po.DictionaryObject()
            form.update(
                {
                    po.NameObject("/Fields"): po.ArrayObject([obj13ref]),
                    po.NameObject("/SigFlags"): po.NumberObject(
                        udct.get("sigflags", 3)
                    ),
                }
            )
        catalog[po.NameObject("/AcroForm")] = form

        if "/Metadata" in catalog:
            catalog[po.NameObject("/Metadata")] = catalog.raw_get("/Metadata")

        x_root = prev.trailer.raw_get("/Root")
        self._objects[x_root.idnum - 1] = catalog
        self.x_root = po.IndirectObject(x_root.idnum, 0, self)
        self.x_info = prev.trailer.get("/Info")


def sign(
    datau,
    udct,
    key,
    cert,
    othercerts,
    algomd="sha1",
    hsm=None,
    timestampurl=None,
    timestampcredentials=None,
    timestamp_req_options=None,
    ocspurl=None,
    ocspissuer=None,
):
    cls = SignedData()
    return cls.sign(
        datau,
        udct,
        key,
        cert,
        othercerts,
        algomd,
        hsm,
        timestampurl,
        timestampcredentials,
        timestamp_req_options,
        "sign",
        ocspurl,
        ocspissuer,
    )
